# Copyright (C) 2006, 2007, 2008 One Laptop Per Child
# Copyright (C) 2009 Simon Schampijer, Aleksey Lim
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import logging

from gettext import gettext as _
import os

import zipfile

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import GObject
from gi.repository import Gdk
from gi.repository import Gtk

# activate threads for gst needs
GObject.threads_init()

import telepathy
import telepathy.client

from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toggletoolbutton import ToggleToolButton
from sugar3.activity.activity import Activity
from sugar3.presence import presenceservice
from sugar3.presence.tubeconn import TubeConnection
from sugar3.graphics import style
from sugar3 import profile

import cardtable
import scoreboard
import game
import messenger
import memorizetoolbar
import createtoolbar
import cardlist
import createcardpanel
import face

SERVICE = 'org.laptop.Memorize'
IFACE = SERVICE
PATH = '/org/laptop/Memorize'

_MODE_PLAY = 1
_MODE_CREATE = 2

# These strings are added only to enable the translators
# to translate the words needed in the stable version
# We can remove them when the version with the new UI is available
# to all the users.

changed_strings = [_('Play'), _('Create'), _('Game name:'), _('Equal pairs'),
                   _('addition'), _('letters'), _('sounds')]


class MemorizeActivity(Activity):

    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.play_mode = None

        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)

        self.activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(self.activity_button, -1)

        self._memorizeToolbarBuilder = \
            memorizetoolbar.MemorizeToolbarBuilder(self)

        toolbar_box.toolbar.insert(Gtk.SeparatorToolItem(), -1)

        self._edit_button = ToggleToolButton('view-source')
        self._edit_button.set_tooltip(_('Edit game'))
        self._edit_button.set_active(False)
        toolbar_box.toolbar.insert(self._edit_button, -1)

        self._createToolbarBuilder = \
            createtoolbar.CreateToolbarBuilder(self)

        separator = Gtk.SeparatorToolItem()
        separator.set_expand(True)
        separator.set_draw(False)
        separator.set_size_request(0, -1)
        toolbar_box.toolbar.insert(separator, -1)

        toolbar_box.toolbar.insert(StopButton(self), -1)

        self.game = game.MemorizeGame()
        # Play game mode
        self.table = cardtable.CardTable()
        self.scoreboard = scoreboard.Scoreboard()
        self.cardlist = cardlist.CardList()
        self.createcardpanel = createcardpanel.CreateCardPanel(self.game)
        self.cardlist.connect('pair-selected',
                              self.createcardpanel.pair_selected)
        self.cardlist.connect(
            'update-create-toolbar',
            self._createToolbarBuilder.update_create_toolbar)
        self.createcardpanel.connect('add-pair',
                                     self.cardlist.add_pair)
        self.createcardpanel.connect('update-pair',
                                     self.cardlist.update_selected)
        self.createcardpanel.connect('change-font',
                                     self.cardlist.change_font)
        self.createcardpanel.connect('pair-closed',
                                     self.cardlist.rem_current_pair)

        self._createToolbarBuilder.connect('create_new_game',
                                           self.cardlist.clean_list)
        self._createToolbarBuilder.connect('create_new_game',
                                           self.createcardpanel.clean)
        self._createToolbarBuilder.connect(
            'create_new_game',
            self._memorizeToolbarBuilder.reset)
        self._createToolbarBuilder.connect('create_equal_pairs',
                                           self.change_equal_pairs)

        self._edit_button.connect('toggled', self._change_mode_bt)

        self.connect('key-press-event', self.table.key_press_event)
        self.table.connect('card-flipped', self.game.card_flipped)
        self.table.connect('card-highlighted', self.game.card_highlighted)

        self.game.connect('set-border', self.table.set_border)
        self.game.connect('flop-card', self.table.flop_card)
        self.game.connect('flip-card', self.table.flip_card)
        self.game.connect('cement-card', self.table.cement_card)
        self.game.connect('highlight-card', self.table.highlight_card)
        self.game.connect('load_mode', self.table.load_msg)

        self.game.connect('msg_buddy', self.scoreboard.set_buddy_message)
        self.game.connect('add_buddy', self.scoreboard.add_buddy)
        self.game.connect('rem_buddy', self.scoreboard.rem_buddy)
        self.game.connect('increase-score', self.scoreboard.increase_score)
        self.game.connect('wait_mode_buddy', self.scoreboard.set_wait_mode)
        self.game.connect('change-turn', self.scoreboard.set_selected)
        self.game.connect('change_game', self.scoreboard.change_game)

        self.game.connect('reset_scoreboard', self.scoreboard.reset)
        self.game.connect('reset_table', self.table.reset)

        self.game.connect('load_game', self.table.load_game)
        self.game.connect('change_game', self.table.change_game)
        self.game.connect('load_game',
                          self._memorizeToolbarBuilder.update_toolbar)
        self.game.connect('change_game',
                          self._memorizeToolbarBuilder.update_toolbar)
        self.game.connect('change_game',
                          self.createcardpanel.update_font_combos)

        self._memorizeToolbarBuilder.connect('game_changed',
                                             self.change_game)

        self.box = Gtk.HBox(orientation=Gtk.Orientation.VERTICAL,
                            homogeneous=False)

        width = Gdk.Screen.width()
        height = Gdk.Screen.height() - style.GRID_CELL_SIZE
        self.table.resize(width, height - style.GRID_CELL_SIZE)
        self.scoreboard.set_size_request(-1, style.GRID_CELL_SIZE)
        self.set_canvas(self.box)

        # connect to the in/out events of the memorize activity
        self.connect('focus_in_event', self._focus_in)
        self.connect('focus_out_event', self._focus_out)
        self.connect('destroy', self._cleanup_cb)

        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.connect('motion_notify_event',
                     lambda widget, event: face.look_at())

        Gdk.Screen.get_default().connect('size-changed',
                                         self.__configure_cb)

        # start on the game toolbar, might change this
        # to the create toolbar later
        self._change_mode(_MODE_PLAY)

        # Get the Presence Service
        self.pservice = presenceservice.get_instance()
        self.initiating = None

        # Buddy object for you
        owner = self.pservice.get_owner()
        self.owner = owner
        self.current = 0

        self.game.set_myself(self.owner)
        self.connect('shared', self._shared_cb)

        # Owner.props.key
        if self.get_shared_activity():
            # We are joining the activity
            self.connect('joined', self._joined_cb)
            if self.get_shared():
                # We've already joined
                self._joined_cb(self)
        elif not self._jobject.file_path:
            logging.debug('buddy joined - __init__: %s', self.owner.props.nick)
            game_file = os.path.join(os.path.dirname(__file__), 'demos',
                                     'addition.zip')
            self.game.load_game(game_file, 4, 'demo')
            logging.debug('loading conventional')
            self.game.add_buddy(self.owner)
        else:
            self.game.add_buddy(self.owner)
        self.show_all()

    def __configure_cb(self, event):
        ''' Screen size has changed '''
        width = Gdk.Screen.width()
        height = Gdk.Screen.height() - style.GRID_CELL_SIZE
        self.box.set_size_request(width, height)
        self.scoreboard.set_size_request(-1, style.GRID_CELL_SIZE)
        self.table.resize(width, height - style.GRID_CELL_SIZE)
        self.show_all()

    def _change_mode_bt(self, button):
        if button.get_active():
            self._change_mode(_MODE_CREATE)
            button.set_icon_name('player_play')
            button.set_tooltip(_('Play game'))
        else:
            self._change_mode(_MODE_PLAY)
            button.set_icon_name('view-source')
            button.set_tooltip(_('Edit game'))

    def read_file(self, file_path):
        if 'icon-color' in self.metadata:
            color = self.metadata['icon-color']
        else:
            color = profile.get_color().to_string()
        self.change_game(None, file_path, 4, 'file',
                         self.metadata['title'], color)

    def write_file(self, file_path):
        logging.debug('WRITE_FILE is_demo %s', self.game.model.is_demo)
        if self.game.model.is_demo:
            # if is a demo game only want keep the metadata
            self._jobject.set_file_path(None)
            raise NotImplementedError
            return
        if self.cardlist.pair_list_modified:
            self.cardlist.update_model(self.game.model)

        temp_img_folder = self.game.model.data['pathimg']
        temp_snd_folder = self.game.model.data['pathsnd']
        self.game.model.create_temp_directories()
        game_zip = zipfile.ZipFile(file_path, 'w')
        save_image_and_sound = True
        if 'origin' in self.game.model.data:
            if self.game.model.data['origin'] == 'art4apps':
                # we don't need save images and audio files
                # for art4apps games
                save_image_and_sound = False

        if save_image_and_sound:
            for pair in self.game.model.pairs:
                # aimg
                aimg = self.game.model.pairs[pair].get_property('aimg')
                if aimg is not None:
                    game_zip.write(os.path.join(temp_img_folder, aimg),
                                   os.path.join('images', aimg))

                # bimg
                bimg = self.game.model.pairs[pair].get_property('bimg')
                if bimg is not None:
                    game_zip.write(os.path.join(temp_img_folder, bimg),
                                   os.path.join('images', bimg))

                # asnd
                asnd = self.game.model.pairs[pair].get_property('asnd')
                if asnd is not None:
                    if os.path.exists(os.path.join(temp_snd_folder, asnd)):
                        game_zip.write(os.path.join(temp_snd_folder, asnd),
                                       os.path.join('sounds', asnd))

                # bsnd
                bsnd = self.game.model.pairs[pair].get_property('bsnd')
                if bsnd is not None:
                    if os.path.exists(os.path.join(temp_snd_folder, bsnd)):
                        game_zip.write(os.path.join(temp_snd_folder, bsnd),
                                       os.path.join('sounds', bsnd))

        self.game.model.game_path = self.game.model.temp_folder
        self.game.model.data['name'] = str(self.get_title())
        self.game.model.write()
        game_zip.write(os.path.join(self.game.model.temp_folder, 'game.xml'),
                       'game.xml')
        game_zip.close()
        self.metadata['mime_type'] = 'application/x-memorize-project'

    def _complete_close(self):
        self._remove_temp_files()
        Activity._complete_close(self)

    def _remove_temp_files(self):
        tmp_root = os.path.join(os.environ['SUGAR_ACTIVITY_ROOT'], 'instance')
        for root, dirs, files in os.walk(tmp_root, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def _change_mode(self, mode):
        logging.debug("Change mode %s" % mode)
        if mode == _MODE_CREATE:
            if self.play_mode:

                self.box.remove(self.scoreboard)
                self.box.remove(self.table)
                self.createcardpanel.update_orientation()
                self.box.pack_start(self.createcardpanel, True, True, 0)
                self.box.pack_start(self.cardlist, False, False, 0)
                self.cardlist.load_game(self.game)
                self.game.model.create_temp_directories()
                self.createcardpanel.set_temp_folder(
                    self.game.model.temp_folder)
            self.play_mode = False
        else:
            if self.game.model.modified:
                self.cardlist.update_model(self.game.model)
                self.save()
                self.game.reset_game()
                self.table.change_game(None, self.game.model.data,
                                       self.game.model.grid)
                self.game.model.modified = False

            if not self.play_mode:
                self.box.remove(self.createcardpanel)
                self.box.remove(self.cardlist)

            if self.play_mode in (False, None):
                self.box.pack_start(self.table, True, True, 0)
                self.box.pack_start(self.scoreboard, False, False, 0)
            self.play_mode = True
        self._memorizeToolbarBuilder.update_controls(mode == _MODE_PLAY)
        self._createToolbarBuilder.update_controls(mode == _MODE_CREATE)

    def change_game(self, widget, game_name, size, mode,
                    title=None, color=None):
        logging.debug('Change game %s', game_name)
        self.game.change_game(widget, game_name, size, mode, title, color)
        self.cardlist.game_loaded = False

    def change_equal_pairs(self, widget, state):
        self.cardlist.update_model(self.game.model)
        self.createcardpanel.change_equal_pairs(widget, state)

    def _shared_cb(self, activity):
        logging.debug('My activity was shared')
        self.initiating = True
        self._sharing_setup()

        logging.debug('This is my activity: making a tube...')
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].OfferDBusTube(
            SERVICE, {})

    def _sharing_setup(self):
        if self.get_shared_activity() is None:
            logging.error('Failed to share or join activity')
            return
        shared_activity = self.get_shared_activity()
        self.conn = shared_activity.telepathy_conn
        self.tubes_chan = shared_activity.telepathy_tubes_chan
        self.text_chan = shared_activity.telepathy_text_chan

        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].connect_to_signal(
            'NewTube', self._new_tube_cb)

        shared_activity.connect('buddy-joined', self._buddy_joined_cb)
        shared_activity.connect('buddy-left', self._buddy_left_cb)

    def _list_tubes_reply_cb(self, tubes):
        for tube_info in tubes:
            self._new_tube_cb(*tube_info)

    def _list_tubes_error_cb(self, e):
        logging.error('ListTubes() failed: %s', e)

    def _joined_cb(self, activity):
        if not self.get_shared_activity():
            return

        logging.debug('Joined an existing shared activity')

        for buddy in self.get_shared_activity().get_joined_buddies():
            if buddy != self.owner:
                logging.debug("buddy joined - _joined_cb: %s  "
                              "(get buddies and add them to my list)",
                              buddy.props.nick)
                self.game.add_buddy(buddy)

        self.game.add_buddy(self.owner)
        self.initiating = False
        self._sharing_setup()

        logging.debug('This is not my activity: waiting for a tube...')
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].ListTubes(
            reply_handler=self._list_tubes_reply_cb,
            error_handler=self._list_tubes_error_cb)

    def _new_tube_cb(self, identifier, initiator, tube_type, service,
                     params, state):
        logging.debug('New tube: ID=%d initator=%d type=%d service=%s '
                      'params=%r state=%d', identifier, initiator, tube_type,
                      service, params, state)

        if (tube_type == telepathy.TUBE_TYPE_DBUS and
                service == SERVICE):
            if state == telepathy.TUBE_STATE_LOCAL_PENDING:
                self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].AcceptDBusTube(
                    identifier)

            self.tube_conn = TubeConnection(
                self.conn,
                self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES], identifier,
                group_iface=self.text_chan[telepathy.CHANNEL_INTERFACE_GROUP])

            self.messenger = messenger.Messenger(self.tube_conn,
                                                 self.initiating,
                                                 self._get_buddy, self.game)
            self.game.connect('flip-card-signal', self.messenger.flip_sender)
            self.game.connect('change_game_signal', self.messenger.change_game)

    def _get_buddy(self, cs_handle):
        """Get a Buddy from a channel specific handle."""
        group = self.text_chan[telepathy.CHANNEL_INTERFACE_GROUP]
        my_csh = group.GetSelfHandle()
        if my_csh == cs_handle:
            handle = self.conn.GetSelfHandle()
        else:
            handle = group.GetHandleOwners([cs_handle])[0]
            assert handle != 0
        return self.pservice.get_buddy_by_telepathy_handle(
            self.tp_conn_name, self.tp_conn_path, handle)

    def _buddy_joined_cb(self, activity, buddy):
        if buddy != self.owner:
            if buddy.props.nick == '':
                logging.debug("buddy joined: empty nick=%s. Will not add.",
                              buddy.props.nick)
            else:
                logging.debug("buddy joined: %s", buddy.props.nick)
                self.game.add_buddy(buddy)

    def _buddy_left_cb(self, activity, buddy):
        if buddy.props.nick == '':
            logging.debug("buddy joined: empty nick=%s. Will not remove",
                          buddy.props.nick)
        else:
            logging.debug("buddy left: %s", buddy.props.nick)
            self.game.rem_buddy(buddy)

    def _focus_in(self, event, data=None):
        self.game.audio.play()

    def _focus_out(self, event, data=None):
        self.game.audio.pause()

    def _cleanup_cb(self, data=None):
        self.game.audio.stop()
