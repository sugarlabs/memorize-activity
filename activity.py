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
import tempfile
import zipfile
import base64
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gdk
from gi.repository import Gtk

# activate threads for gst needs
GObject.threads_init()

from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toggletoolbutton import ToggleToolButton
from sugar3.activity.activity import Activity
from sugar3.graphics import style
from sugar3 import profile

import cardtable
import scoreboard
import game
import memorizetoolbar
import createtoolbar
import cardlist
import createcardpanel
import face
from collabwrapper import CollabWrapper

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

        def on_activity_joined_cb(me):
            logging.debug('activity joined')
            self.game.add_buddy(self._collab.props.owner)
        self.connect('joined', on_activity_joined_cb)

        def on_activity_shared_cb(me):
            logging.debug('activity shared')
        self.connect('shared', on_activity_shared_cb)

        self._collab = CollabWrapper(self)
        self.game.set_myself(self._collab.props.owner)

        def on_message_cb(collab, buddy, msg):
            logging.debug('on_message_cb buddy %r msg %r' % (buddy, msg))
            action = msg.get('action')
            if action == 'flip':
                n = msg.get('n')
                self.game.card_flipped(None, n, True)
            elif action == 'change':
                self.get_canvas().hide()

                def momentary_blank_timeout_cb():
                    self.set_data(msg)
                    self.get_canvas().show()
                GLib.timeout_add(100, momentary_blank_timeout_cb)

        self._collab.connect('message', on_message_cb)

        def on_joined_cb(collab, msg):
            logging.debug('joined')
        self._collab.connect('joined', on_joined_cb, 'joined')

        def on_buddy_joined_cb(collab, buddy, msg):
            logging.debug('on_buddy_joined_cb buddy %r msg %r' % (buddy, msg))
            self.game.add_buddy(buddy)

        self._collab.connect('buddy_joined', on_buddy_joined_cb,
                             'buddy_joined')

        def on_buddy_left_cb(collab, buddy, msg):
            logging.debug('on_buddy_left_cb buddy %r msg %r' % (buddy, msg))
            self.game.rem_buddy(buddy)

        self._collab.connect('buddy_left', on_buddy_left_cb, 'buddy_left')

        self._files = {}  # local temporary copies of shared games

        self._collab.setup()

        def on_flip_card_cb(game, n):
            logging.debug('on_flip_card_cb n %r' % (n))
            self._collab.post({'action': 'flip', 'n': n})

        self.game.connect('flip-card-signal', on_flip_card_cb)

        def on_change_game_cb(sender, mode, grid, data, waiting_list, zip):
            logging.debug('on_change_game_cb')
            blob = self.get_data()
            blob['action'] = 'change'

            self._collab.post(blob)

        self.game.connect('change_game_signal', on_change_game_cb)

        if self._collab.props.leader:
            logging.debug('is leader')
            game_file = os.path.join(os.path.dirname(__file__), 'demos',
                                     'addition.zip')
            self.game.load_game(game_file, 4, 'demo')
            self.game.add_buddy(self._collab.props.owner)

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

    def _change_game_receiver(self, mode, grid, data, path):
        if mode == 'demo':
            game_name = os.path.basename(data.get('game_file', 'debug-demo'))
            game_file = os.path.join(
                os.path.dirname(__file__), 'demos', game_name).encode('ascii')
            self.game.model.read(game_file)

        if mode == 'art4apps':
            game_file = data['game_file']
            category = game_file[:game_file.find('_')]
            language = data['language']
            self.game.model.is_demo = True
            self.game.model.read_art4apps(category, language)

        if mode == 'file':
            self.game.model.read(self._files[path])

        if 'path' in self.game.model.data:
            data['path'] = self.game.model.data['path']
            data['pathimg'] = self.game.model.data['pathimg']
            data['pathsnd'] = self.game.model.data['pathsnd']
        self.game.load_remote(grid, data, mode, True)

    def set_data(self, blob):
        logging.debug("set_data %r" % list(blob.keys()))
        grid = blob['grid']
        data = blob['data']
        current_player = blob['current']
        path = blob['path']

        if 'zip' in blob:
            tmp_root = os.path.join(os.environ['SUGAR_ACTIVITY_ROOT'],
                                    'instance')
            temp_dir = tempfile.mkdtemp(dir=tmp_root)
            os.chmod(temp_dir, 0o777)
            temp_file = os.path.join(temp_dir, 'game.zip')
            self._files[path] = temp_file
            f = open(temp_file, 'wb')

            f.write(base64.b64decode(blob['zip']))
            f.close()

        self._change_game_receiver(data['mode'], grid, data, path)

        for i in range(len(self.game.players)):
            self.game.increase_point(self.game.players[i],
                                     int(data.get(str(i), '0')))

        self.game.current_player = self.game.players[current_player]
        self.game.update_turn()

    def get_data(self):
        data = self.game.collect_data()
        path = data['game_file']

        blob = {"grid": self.game.get_grid(),
                "data": data,
                "current": self.game.players.index(self.game.current_player),
                "path": path}

        if data['mode'] == 'file':
            blob['zip'] = base64.b64encode(open(path, 'rb').read()).decode()

        logging.debug("get_data %r" % list(blob.keys()))
        return blob

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

    def _focus_in(self, event, data=None):
        self.game.audio.play()

    def _focus_out(self, event, data=None):
        self.game.audio.pause()

    def _cleanup_cb(self, data=None):
        self.game.audio.stop()
