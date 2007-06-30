#! /usr/bin/env python
#
#    Copyright (C) 2006 Simon Schampijer
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

from gettext import gettext as _

import gobject
import gtk
import os
import logging
import dbus
import telepathy
import telepathy.client

from sugar.activity.activity import Activity
from sugar.activity.activity import ActivityToolbox
from sugar.presence import presenceservice

from csound.csoundserver import CsoundServer
from playview import PlayView
#from toolbar import PlayToolbar
from model import Game
from game import ConnectGame

class MemosonoActivity(Activity):
    def __init__(self, handle):
        Activity.__init__(self, handle)
        self.set_title ("Memosono")

        self.pv = None
        toolbox = ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()
                
        self.games = {}

        os.path.walk(os.path.join(os.path.dirname(__file__), 'games'), self._find_games, None)

        gamelist = self.games.keys()
        gamelist.sort()
        logging.debug(gamelist)
        self.pv = PlayView(None, self.games[gamelist[0]].pairs)
        self.pv.show()
        
        self.pservice = presenceservice.get_instance()
        self.owner = self.pservice.get_owner()

        bus = dbus.Bus()
        name, path = self.pservice.get_preferred_connection()
        self.tp_conn_name = name
        self.tp_conn_path = path
        self.conn = telepathy.client.Connection(name, path)
        self.initiating = None
        self.game = None
        
        self.connect('shared', self._shared_cb)

        if self._shared_activity:
            # we are joining the activity
            self.buddies_panel.add_watcher(owner)
            self.connect('joined', self._joined_cb)
            self._shared_activity.connect('buddy-joined', self._buddy_joined_cb)
            self._shared_activity.connect('buddy-left', self._buddy_left_cb)
            if self.get_shared():
                # oh, OK, we've already joined
                self._joined_cb()
        else:
            # we are creating the activity
            self.pv.buddies_panel .add_player(self.owner)


    def _shared_cb(self, activity):
        logging.debug('My Memosono activity was shared')
        self.initiating = True
        self._setup()

        for buddy in self._shared_activity.get_joined_buddies():
            self.pv.buddies_panel.add_watcher(buddy)

        self._shared_activity.connect('buddy-joined', self._buddy_joined_cb)
        self._shared_activity.connect('buddy-left', self._buddy_left_cb)

        logging.debug('This is my activity: making a tube...')
        id = self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].OfferTube(
            telepathy.TUBE_TYPE_DBUS, 'org.fredektop.Telepathy.Tube.Memosono', {})
        logging.debug('Tube address: %s', self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].GetDBusServerAddress(id))
        logging.debug('Waiting for another player to join')

    # FIXME: presence service should be tubes-aware and give us more help
    # with this
    def _setup(self):
        if self._shared_activity is None:
            logging.error('Failed to share or join activity')
            return

        bus_name, conn_path, channel_paths = self._shared_activity.get_channels()

        # Work out what our room is called and whether we have Tubes already
        room = None
        tubes_chan = None
        text_chan = None
        for channel_path in channel_paths:
            channel = telepathy.client.Channel(bus_name, channel_path)
            htype, handle = channel.GetHandle()
            if htype == telepathy.HANDLE_TYPE_ROOM:
                logging.debug('Found our room: it has handle#%d "%s"',
                    handle, self.conn.InspectHandles(htype, [handle])[0])
                room = handle
                ctype = channel.GetChannelType()
                if ctype == telepathy.CHANNEL_TYPE_TUBES:
                    logging.debug('Found our Tubes channel at %s', channel_path)
                    tubes_chan = channel
                elif ctype == telepathy.CHANNEL_TYPE_TEXT:
                    logging.debug('Found our Text channel at %s', channel_path)
                    text_chan = channel

        if room is None:
            logging.error("Presence service didn't create a room")
            return
        if text_chan is None:
            logging.error("Presence service didn't create a text channel")
            return

        # Make sure we have a Tubes channel - PS doesn't yet provide one
        if tubes_chan is None:
            logging.debug("Didn't find our Tubes channel, requesting one...")
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
        logging.error('ListTubes() failed: %s', e)

    def _joined_cb(self, activity):
        if self.game is not None:
            return

        if not self._shared_activity:
            return

        for buddy in self._shared_activity.get_joined_buddies():
            self.pv.buddies_panel.add_watcher(buddy)

        logging.debug('Joined an existing Connect game')
        logging.debug('Joined a game. Waiting for my turn...')
        self.initiating = False
        self._setup()

        logging.debug('This is not my activity: waiting for a tube...')
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].ListTubes(
            reply_handler=self._list_tubes_reply_cb,
            error_handler=self._list_tubes_error_cb)

    def _new_tube_cb(self, id, initiator, type, service, params, state):
        logging.debug('New tube: ID=%d initator=%d type=%d service=%s '
                     'params=%r state=%d', id, initiator, type, service,
                     params, state)

        if (self.game is None and type == telepathy.TUBE_TYPE_DBUS and
            service == 'org.fredektop.Telepathy.Tube.Memosono'):
            if state == telepathy.TUBE_STATE_LOCAL_PENDING:
                self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].AcceptTube(id)

            tube_conn = TubeConnection(self.conn,
                self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES],
                id, group_iface=self.text_chan[telepathy.CHANNEL_INTERFACE_GROUP])
            self.game = ConnectGame(tube_conn, self.grid, self.initiating,
                self.pv.buddies_panel, self.info_panel, self.owner,
                self._get_buddy, self)

    def _buddy_joined_cb (self, activity, buddy):
        logging.debug('buddy joined')
        self.pv.buddies_panel.add_watcher(buddy)

    def _buddy_left_cb (self,  activity, buddy):
        logging.debug('buddy left')
        self.pv.buddies_panel.remove_watcher(buddy)
        
        
    def _find_games(self, arg, dirname, names):
        for name in names:
            if name.endswith('.mson'): 
                game = Game(dirname, os.path.dirname(__file__))
                game.read(name)
                self.games[name.split('.mson')[0]] = game
                
    def _cleanup_cb(self, data=None):
        pass
        #self.controler.oscapi.send(('127.0.0.1', 6783), "/CSOUND/quit", [])
        #self.controler.oscapi.iosock.close()
        #self.server.oscapi.iosock.close()
        #logging.debug(" Closed OSC sockets ")
        
    def _focus_in(self, event, data=None):
        pass
        #logging.debug(" Memosono is visible: Connect to the Csound-Server. ")
        #self.controler.oscapi.send(('127.0.0.1', 6783), "/CSOUND/connect", [])
        
    def _focus_out(self, event, data=None):
        pass
        #logging.debug(" Memosono is invisible: Close the connection to the Csound-Server. ")
        #self.controler.oscapi.send(('127.0.0.1', 6783), "/CSOUND/disconnect", [])
