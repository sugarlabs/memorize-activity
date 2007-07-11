#! /usr/bin/env python
#
#    Copyright (C) 2006, 2007 Simon Schampijer
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
import telepathy
import telepathy.client
import hippo

from sugar.activity.activity import Activity
from sugar.activity.activity import ActivityToolbox
from sugar.presence import presenceservice

from tubeconn import TubeConnection
from playview import PlayView
from buddiespanel import BuddiesPanel
from infopanel import InfoPanel
from controller import Controller


_logger = logging.getLogger('activity')

class MemosonoActivity(Activity):
    def __init__(self, handle):
        Activity.__init__(self, handle)

        _logger.debug('Starting Memosono activity...')

        self.set_title(_('Memsosono Activity'))

        w = self.get_screen().get_width()
        h = self.get_screen().get_height()
        ### FIXME: do better grid calculation
        if w <= 1024:            
            self.pv = PlayView(600, 600, 32)
        else:            
            self.pv = PlayView(800, 800, 32)

        self.buddies_panel = BuddiesPanel()

        self.info_panel = InfoPanel()

        vbox = hippo.CanvasBox(spacing=4,
                               orientation=hippo.ORIENTATION_VERTICAL)

        hbox = hippo.CanvasBox(spacing=4,
                               orientation=hippo.ORIENTATION_HORIZONTAL)

        hbox.append(self.buddies_panel)
        hbox.append(self.pv, hippo.PACK_EXPAND)
        
        vbox.append(hbox, hippo.PACK_EXPAND)
        vbox.append(self.info_panel, hippo.PACK_END)

        canvas = hippo.Canvas()
        canvas.set_root(vbox)
        self.set_canvas(canvas)
        self.show_all()
        
        toolbox = ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()

        self.pservice = presenceservice.get_instance()

        name, path = self.pservice.get_preferred_connection()
        self.tp_conn_name = name
        self.tp_conn_path = path
        self.conn = telepathy.client.Connection(name, path)
        self.initiating = None

        self.ctrl = None

        toolbox = ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()

        # connect to the in/out events of the memosono activity
        self.connect('focus_in_event', self._focus_in)
        self.connect('focus_out_event', self._focus_out)
        self.connect('destroy', self._cleanup_cb)
        
        self.info_panel.show('To play, share!')

        self.connect('shared', self._shared_cb)

        owner = self.pservice.get_owner()
        self.owner = owner

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
            self.buddies_panel.add_player(owner)
            
    def _get_buddy(self, cs_handle):
        """Get a Buddy from a channel specific handle."""
        _logger.debug('Trying to find owner of handle %u...', cs_handle)
        group = self.text_chan[telepathy.CHANNEL_INTERFACE_GROUP]
        my_csh = group.GetSelfHandle()
        _logger.debug('My handle in that group is %u', my_csh)
        if my_csh == cs_handle:
            handle = self.conn.GetSelfHandle()
            _logger.debug('CS handle %u belongs to me, %u', cs_handle, handle)
        elif group.GetGroupFlags() & telepathy.CHANNEL_GROUP_FLAG_CHANNEL_SPECIFIC_HANDLES:
            handle = group.GetHandleOwners([cs_handle])[0]
            _logger.debug('CS handle %u belongs to %u', cs_handle, handle)
        else:
            handle = cs_handle
            _logger.debug('non-CS handle %u belongs to itself', handle)

            # XXX: deal with failure to get the handle owner
            assert handle != 0

        # XXX: we're assuming that we have Buddy objects for all contacts -
        # this might break when the server becomes scalable.
        return self.pservice.get_buddy_by_telepathy_handle(self.tp_conn_name,
                self.tp_conn_path, handle)

    def _shared_cb(self, activity):
        _logger.debug('My Memosono activity was shared')
        self.initiating = True
        self._setup()

        for buddy in self._shared_activity.get_joined_buddies():
            self.buddies_panel.add_watcher(buddy)

        self._shared_activity.connect('buddy-joined', self._buddy_joined_cb)
        self._shared_activity.connect('buddy-left', self._buddy_left_cb)

        _logger.debug('This is my activity: making a tube...')
        id = self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].OfferTube(
            telepathy.TUBE_TYPE_DBUS, 'org.fredektop.Telepathy.Tube.Memosono', {})
        _logger.debug('Tube address: %s', self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].GetDBusServerAddress(id))
        self.info_panel.show('Waiting for another player to join')

    # FIXME: presence service should be tubes-aware and give us more help
    # with this
    def _setup(self):
        if self._shared_activity is None:
            _logger.error('Failed to share or join activity')
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
        if self.ctrl is not None:
            return

        if not self._shared_activity:
            return

        for buddy in self._shared_activity.get_joined_buddies():
            self.buddies_panel.add_watcher(buddy)

        _logger.debug('Joined an existing Memosono game')
        self.info_panel.show('Joined a game. Waiting for my turn...')
        self.initiating = False
        self._setup()

        _logger.debug('This is not my activity: waiting for a tube...')
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].ListTubes(
            reply_handler=self._list_tubes_reply_cb,
            error_handler=self._list_tubes_error_cb)

    def _new_tube_cb(self, id, initiator, type, service, params, state):
        _logger.debug('New tube: ID=%d initator=%d type=%d service=%s '
                     'params=%r state=%d', id, initiator, type, service,
                     params, state)

        if (self.ctrl is None and type == telepathy.TUBE_TYPE_DBUS and
            service == 'org.fredektop.Telepathy.Tube.Memosono'):
            if state == telepathy.TUBE_STATE_LOCAL_PENDING:
                self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].AcceptTube(id)

            tube_conn = TubeConnection(self.conn,
                self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES],
                id, group_iface=self.text_chan[telepathy.CHANNEL_INTERFACE_GROUP])
            self.ctrl = Controller(tube_conn, self.pv, self.initiating,
                self.buddies_panel, self.info_panel, self.owner,
                self._get_buddy, self)

    def _buddy_joined_cb(self, activity, buddy):
        _logger.debug('buddy joined')
        self.buddies_panel.add_watcher(buddy)

    def _buddy_left_cb(self,  activity, buddy):
        _logger.debug('buddy left')
        self.buddies_panel.remove_watcher(buddy)
                        
    def write_file(self, file_path):
        """Store game state in Journal.

        Handling the Journal is provided by Activity - we only need
        to define this method.
        """
        _logger.debug(" Write game state. ")
        f = open(file_path, 'w')
        try:
            f.write('erikos won the game')
        finally:
            f.close()

    def _focus_in(self, event, data=None):
        if self.ctrl != None:
            self.ctrl.cs.start()
            _logger.debug(" Memosono is visible: start csound server. ")
        
    def _focus_out(self, event, data=None):
        if self.ctrl != None:
            self.ctrl.cs.start()
            _logger.debug(" Memosono is invisible: pause csound server. ")
        
    def _cleanup_cb(self, data=None):
        if self.ctrl != None:
            self.ctrl.cs.quit()        
            _logger.debug(" Memosono closes: close csound server. ")

