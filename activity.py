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
import os

import dbus
import gtk
import pygtk
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

from sugar.presence.tubeconn import TubeConnection

SERVICE = "org.laptop.Memorize"
IFACE = SERVICE
PATH = "/org/laptop/Memorize"

_logger = logging.getLogger('memorize-activity')

class MemorizeActivity(Activity):
    def __init__(self, handle):
        Activity.__init__(self, handle)
        
        self.set_title(_('Memorize Activity'))

        self.table = cardtable.CardTable()
        self.scoreboard = scoreboard.Scoreboard()
        self.game = game.MemorizeGame()
        
        hbox = gtk.HBox(False)
        hbox.pack_start(self.scoreboard, False, False)
        hbox.pack_start(self.table)

        toolbox = ActivityToolbox(self)
        activity_toolbar = toolbox.get_activity_toolbar()
        
        self._memorizeToolbar = memorizetoolbar.MemorizeToolbar(self)
        toolbox.add_toolbar(_('Games'), self._memorizeToolbar)
        self._memorizeToolbar.show()
        
        self.set_toolbox(toolbox)
        toolbox.show()
        self.set_canvas(hbox)
        
        self.table.connect('key-press-event', self.table.key_press_event)        
        self.connect('shared', self._shared_cb)
        
        self.table.connect('card-flipped', self.game.card_flipped)
        self.table.connect('card-highlighted', self.game.card_highlighted)

        self.game.connect('reset_scoreboard', self.scoreboard.reset)
        self.game.connect('reset_table', self.table.reset)
        self.game.connect('load_game', self.table.load_game)
        self.game.connect('change_game', self.table.change_game)
        self.game.connect('load_game', self._memorizeToolbar.update_toolbar)
        self.game.connect('change_game', self._memorizeToolbar.update_toolbar)
        self.game.connect('set-border', self.table.set_border)
        self.game.connect('flop-card', self.table.flop_card)
        self.game.connect('flip-card', self.table.flip_card)
        self.game.connect('highlight-card', self.table.highlight_card)
        self.game.connect('add_buddy', self.scoreboard.add_buddy)
        self.game.connect('rem_buddy', self.scoreboard.rem_buddy)
        self.game.connect('increase-score', self.scoreboard.increase_score)
        self.game.connect('wait_mode_buddy', self.scoreboard.set_wait_mode)
        self.game.connect('change-turn', self.scoreboard.set_selected)
        
        self.show_all()
        
        # connect to the in/out events of the memorize activity
        self.connect('focus_in_event', self._focus_in)
        self.connect('focus_out_event', self._focus_out)
        self.connect('destroy', self._cleanup_cb)

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
        self.game.set_myself(self.owner)
        # Owner.props.key
        if self._shared_activity:
            # We are joining the activity
            # _logger.debug("Joined activity, add myself to buddy list nick=%s" %self.owner.props.nick)          
            # self.game.add_buddy(self.owner)
            self.connect('joined', self._joined_cb)
            if self.get_shared():
                # We've already joined
                self._joined_cb()
        else:
            _logger.debug("buddy joined - __init__: %s", self.owner.props.nick)
            self.game.load_game('addition', 4)
            self.game.add_buddy(self.owner)
            
    def restart(self, widget):
        self.game.reset()

    def change_game(self, game_name, size):
        self.game.change_game(game_name, size)
        
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
            self.game.connect('flip-card-signal', self.messenger.flip)
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
        if self.game.sound == 1:
            self.game.cs.start()
            _logger.debug(" Memorize is visible: start csound server. ")
        
    def _focus_out(self, event, data=None):
        if self.game.sound == 1:
            self.game.cs.pause()
            _logger.debug(" Memorize is invisible: pause csound server. ")
        
    def _cleanup_cb(self, data=None):
        if self.game.sound == 1:
            self.game.cs.quit()        
            _logger.debug(" Memorize closes: close csound server. ")
