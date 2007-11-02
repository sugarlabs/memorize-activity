#! /usr/bin/env python
#
#    Copyright (C) 2006, 2007, One Laptop Per Child
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

import logging
from gettext import gettext as _
from os.path import join, dirname

import dbus
import gtk
import pygtk
import pickle
import telepathy
import telepathy.client

from sugar.activity.activity import Activity, ActivityToolbox
from sugar.presence import presenceservice
import sugar.logger

from sugar.graphics.xocolor import XoColor
from sugar import profile
import cardtable
import scoreboard
import game
import messenger
import memorizetoolbar
import createtoolbar
import cardlist
import createcardpanel

from sugar.presence.tubeconn import TubeConnection

SERVICE = 'org.laptop.Memorize'
IFACE = SERVICE
PATH = '/org/laptop/Memorize'

_TOOLBAR_CREATE = 1
_TOOLBAR_PLAY = 2

_logger = logging.getLogger('memorize-activity')

class MemorizeActivity(Activity):
    
    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.play_load = False
        self.play_mode = False
        
        toolbox = ActivityToolbox(self)
        toolbox.connect('current-toolbar-changed', self.change_mode)
        activity_toolbar = toolbox.get_activity_toolbar()
        
        self._createToolbar = createtoolbar.CreateToolbar(self)
        toolbox.add_toolbar('Create', self._createToolbar)
        self._createToolbar.show()
        
        self._memorizeToolbar = memorizetoolbar.MemorizeToolbar(self)
        toolbox.add_toolbar(_('Play'), self._memorizeToolbar)
        self._memorizeToolbar.show()   

        self.set_toolbox(toolbox)
        toolbox.show()
        
        self.cardlist = cardlist.CardList()
        self.createcardpanel = createcardpanel.CreateCardPanel()
        self.createcardpanel.connect('add-pair', self.cardlist.add_pair)
        self.createcardpanel.connect('update-pair', self.cardlist.update_selected)
        self.cardlist.connect('pair-selected', self.createcardpanel.load_pair)
        self.cardlist.connect('update-create-toolbar', self._createToolbar.update_create_toolbar)
        self.cardlist.connect('update-create-buttons', self._createToolbar.update_buttons_status)
        self._createToolbar.connect('create_new_game', self.cardlist.clean_list)
        self._createToolbar.connect('create_new_game', self.createcardpanel.clean)
        self._createToolbar.connect('create_load_game', self.cardlist.load_game)
        self._createToolbar.connect('create_save_game', self.cardlist.save_game)
        self._createToolbar.connect('create_equal_pairs', self.createcardpanel.change_equal_pairs)       
        
        self.hbox = gtk.HBox(False)
        self.hbox.pack_start(self.createcardpanel)
        self.hbox.pack_start(self.cardlist, False, False)
        self.set_canvas(self.hbox)
        
       # create csound instance to play sound files
        self.sound = 0        
        try:
            import csnd
            del csnd
            self.sound = 1
        except:
            self.sound = 0

        if self.sound == 1:
            from csound.csoundserver import CsoundServer            
            cs = CsoundServer()        
            if cs.start() != 0:
                self.sound = 0
            else:
                cs.quit()

        # connect to the in/out events of the memorize activity
        self.connect('focus_in_event', self._focus_in)
        self.connect('focus_out_event', self._focus_out)
        self.connect('destroy', self._cleanup_cb)

        # start on the game toolbar, might change this to the create toolbar later
        self.toolbox.set_current_toolbar(_TOOLBAR_CREATE)
        
        # Get the Presence Service
        self.pservice = presenceservice.get_instance()
        try:
            name, path = self.pservice.get_preferred_connection()
            self.tp_conn_name = name
            self.tp_conn_path = path
            self.conn = telepathy.client.Connection(name, path)            
        except TypeError:
            _logger.debug('Offline')
        self.initiating = None
            
        # Buddy object for you
        owner = self.pservice.get_owner()
        self.owner = owner
        self.current = 0
        # Owner.props.key
        if self._shared_activity:
            # We are joining the activity
            self.toolbox.set_current_toolbar(_TOOLBAR_PLAY)
            self.connect('joined', self._joined_cb)
            if self.get_shared():
                # We've already joined
                self._joined_cb()
        else:
            _logger.debug('buddy joined - __init__: %s', self.owner.props.nick)
            #game_file = join(dirname(__file__),'demos','addition.zip')
            #self.game.load_game(game_file, 4)
            _logger.debug('loading conventional')       
            #self.game.add_buddy(self.owner)
        self.show_all()
        
    def read_file(self, file_path):
        '''
        if self.metadata['mime_type'] == 'plain/text':
            f = open(file_path, 'r')
            try:
                data = pickle.load(f)
            finally:
                f.close()

            _logger.debug('reading from datastore')            
            
            self.game.load_remote(data[0], data[1])
            self.game.set_wait_list(data[2])
        '''
        if self.metadata['mime_type'] == 'application/memorizegame':
            self.toolbox.set_current_toolbar(_TOOLBAR_PLAY)
            self.game.change_game(None, file_path, 4, 'file', self.metadata['title'], self.metadata['icon-color'])
            
    '''
    def write_file(self, file_path):
        if not self.metadata['mime_type']:
            self.metadata['mime_type'] = 'plain/text'
        
        if self.metadata['mime_type'] == 'plain/text':
       
            
            data=[self.game.get_grid(), self.game.get_data(), self.game.get_players_data()]
            
            _logger.debug('writing to datastore')
            f = open(file_path, 'w')
            try:
                pickle.dump(data, f)
            finally:
                f.close()
    '''
    def change_mode(self, notebook, index):
        if index != _TOOLBAR_CREATE:
            if not self.play_load:
                # Create play components
                self.table = cardtable.CardTable()
                self.scoreboard = scoreboard.Scoreboard()
                self.game = game.MemorizeGame()
                self.game.set_myself(self.owner)  
                self.hbox.remove(self.createcardpanel)
                self.hbox.remove(self.cardlist)
                self.hbox.pack_start(self.scoreboard, False, False)
                self.hbox.pack_start(self.table)
                
                self.table.connect('key-press-event', self.table.key_press_event)        
                self.table.connect('card-flipped', self.game.card_flipped)
                self.table.connect('card-highlighted', self.game.card_highlighted)
                
                self.game.connect('set-border', self.table.set_border)
                self.game.connect('flop-card', self.table.flop_card)
                self.game.connect('flip-card', self.table.flip_card)
                self.game.connect('highlight-card', self.table.highlight_card)
                self.game.connect('load_mode', self.table.load_msg)
                
                self.game.connect('msg_buddy', self.scoreboard.set_buddy_message)
                self.game.connect('add_buddy', self.scoreboard.add_buddy)
                self.game.connect('rem_buddy', self.scoreboard.rem_buddy)
                self.game.connect('increase-score', self.scoreboard.increase_score)
                self.game.connect('wait_mode_buddy', self.scoreboard.set_wait_mode)
                self.game.connect('change-turn', self.scoreboard.set_selected)
                
                self.game.connect('reset_scoreboard', self.scoreboard.reset)
                self.game.connect('reset_table', self.table.reset)
                
                self.game.connect('load_game', self.table.load_game)
                self.game.connect('change_game', self.table.change_game)
                self.game.connect('load_game', self._memorizeToolbar.update_toolbar)
                self.game.connect('change_game', self._memorizeToolbar.update_toolbar)
                
                self._memorizeToolbar.connect('game_changed', self.game.change_game)
                self.connect('shared', self._shared_cb)
                self.play_load = True
                if not self._shared_activity:
                    self.game.add_buddy(self.owner)
                    #game_file = join(dirname(__file__), 'demos', 'addition.zip')
                    #self.game.load_game(game_file, 4)
            else:
                self.hbox.remove(self.createcardpanel)
                self.hbox.remove(self.cardlist)
                self.hbox.pack_start(self.scoreboard, False, False)
                self.hbox.pack_start(self.table)
            self.play_mode = True
        else:            
            if self.play_mode:
                self.hbox.remove(self.scoreboard)
                self.hbox.remove(self.table)
                self.hbox.pack_start(self.createcardpanel)
                self.hbox.pack_start(self.cardlist, False, False)
                self.play_mode = False
                
    def restart(self, widget):
        self.game.reset()

    def change_game(self, game_name, size, title=None, color=None):
        self.game.change_game(game_name, size, title, color)
        
    def _shared_cb(self, activity):
        _logger.debug('My activity was shared')
        self.initiating = True
        self._setup()

        for buddy in self._shared_activity.get_joined_buddies():
            pass  # Can do stuff with newly acquired buddies here

        self._shared_activity.connect('buddy-joined', self._buddy_joined_cb)
        self._shared_activity.connect('buddy-left', self._buddy_left_cb)

        _logger.debug('This is my activity: making a tube...')
        id = self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].OfferDBusTube(
            SERVICE, {})

    def _setup(self):
        if self._shared_activity is None:
            _logger.error('Failed to share or join activity')
            return

        bus_name, conn_path, channel_paths =\
            self._shared_activity.get_channels()

        # Work out what our room is called and whether we have Tubes already
        room = None
        tubes_chan = None
        text_chan = None
        for channel_path in channel_paths:
            channel = telepathy.client.Channel(bus_name, channel_path)
            htype, handle = channel.GetHandle()
            if htype == telepathy.HANDLE_TYPE_ROOM:
                _logger.debug('Found our room: it has handle#%d "%s"', 
                    handle, self.conn.InspectHandles(htype, [handle])[0])
                room = handle
                ctype = channel.GetChannelType()
                if ctype == telepathy.CHANNEL_TYPE_TUBES:
                    _logger.debug('Found our Tubes channel at %s', channel_path)
                    tubes_chan = channel
                elif ctype == telepathy.CHANNEL_TYPE_TEXT:
                    _logger.debug('Found our Text channel at %s', channel_path)
                    text_chan = channel

        if room is None:
            _logger.error("Presence service didn't create a room")
            return
        if text_chan is None:
            _logger.error("Presence service didn't create a text channel")
            return

        # Make sure we have a Tubes channel - PS doesn't yet provide one
        if tubes_chan is None:
            _logger.debug("Didn't find our Tubes channel, requesting one...")
            tubes_chan = self.conn.request_channel(telepathy.CHANNEL_TYPE_TUBES, 
                telepathy.HANDLE_TYPE_ROOM, room, True)

        self.tubes_chan = tubes_chan
        self.text_chan = text_chan

        tubes_chan[telepathy.CHANNEL_TYPE_TUBES].connect_to_signal('NewTube', 
            self._new_tube_cb)

    def _list_tubes_reply_cb(self, tubes):
        for tube_info in tubes:
            self._new_tube_cb(*tube_info)

    def _list_tubes_error_cb(self, e):
        _logger.error('ListTubes() failed: %s', e)

    def _joined_cb(self, activity):
        if not self._shared_activity:
            return

        _logger.debug('Joined an existing shared activity')

        self.found = 0
        for buddy in self._shared_activity.get_joined_buddies():
            _logger.debug("buddy joined - _joined_cb: %s  (get buddies of activity and add them to my list)", buddy.props.nick)
            self.game.add_buddy(buddy)
            if buddy == self.owner:
                self.found = 1

        if self.found == 0:
            _logger.debug("buddy joined - _joined_cb: Not foud myself in buddy list - will add myself at end of the list.")
            self.game.add_buddy(self.owner)

        self.initiating = False
        self._setup()
        
        self._shared_activity.connect('buddy-joined', self._buddy_joined_cb)
        self._shared_activity.connect('buddy-left', self._buddy_left_cb)

        _logger.debug('This is not my activity: waiting for a tube...')
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].ListTubes(
            reply_handler=self._list_tubes_reply_cb, 
            error_handler=self._list_tubes_error_cb)

    def _new_tube_cb(self, id, initiator, type, service, params, state):
        _logger.debug('New tube: ID=%d initator=%d type=%d service=%s '
                     'params=%r state=%d', id, initiator, type, service, 
                     params, state)

        if (type == telepathy.TUBE_TYPE_DBUS and
            service == SERVICE):
            if state == telepathy.TUBE_STATE_LOCAL_PENDING:
                self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].AcceptDBusTube(id)

            self.tube_conn = TubeConnection(self.conn, 
                self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES], 
                id, group_iface=self.text_chan[telepathy.CHANNEL_INTERFACE_GROUP])
            
            self.messenger = messenger.Messenger(self.tube_conn, self.initiating, self._get_buddy, self.game)         
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
         return self.pservice.get_buddy_by_telepathy_handle(self.tp_conn_name, 
                 self.tp_conn_path, handle)
             
    def _buddy_joined_cb (self, activity, buddy):
        if buddy <> self.owner:
            if buddy.props.nick == '':
                _logger.debug("buddy joined - _buddy_joined_cb: buddy name empty nick=%s. Will not add." %(buddy.props.nick))
            else:
                _logger.debug("buddy joined - _buddy_joined_cb: %s", buddy.props.nick)
                self.game.add_buddy(buddy)

    def _buddy_left_cb (self, activity, buddy):
        if buddy.props.nick == '':
            _logger.debug("buddy joined - _buddy_left_cb: buddy name empty nick=%s. Will not remove" %(buddy.props.nick))
        else:
            _logger.debug("buddy left - _buddy_left_cb: %s", buddy.props.nick)
            self.game.rem_buddy(buddy)

    def _focus_in(self, event, data=None):
        if self.sound == 1:
            pass
            #self.game.cs.start()
            #_logger.debug(" Memorize is visible: start csound server. ")
        
    def _focus_out(self, event, data=None):
        if self.sound == 1:
            pass
            #self.game.cs.pause()
            #_logger.debug(" Memorize is invisible: pause csound server. ")
        
    def _cleanup_cb(self, data=None):
        if self.sound == 1:
            pass
            #self.game.cs.quit()        
            #_logger.debug(" Memorize closes: close csound server. ")
