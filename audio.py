# Copyright (C) 2006, 2007, 2008 One Laptop per Child
# Copyright (C) 2013, Ignacio Rodriguez
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

from gi.repository import Gst
from gi.repository import GObject

import logging

Gst.init([])


class Audio(GObject.GObject):

    __gsignals__ = {
        'play_finished': (GObject.SignalFlags.RUN_FIRST, None, []), }

    def __init__(self):
        GObject.GObject.__init__(self)
        self._player = Gst.ElementFactory.make('playbin', 'player')
        fakesink = Gst.ElementFactory.make('fakesink', 'my-fakesink')
        self._player.set_property('video-sink', fakesink)
        self._playing = None

        bus = self._player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._gstmessage_cb)

    def play(self, filename=None):
        if filename:
            logging.debug('play audio %s' % filename)
            self._player.set_state(Gst.State.NULL)
            self._player.set_property('uri', 'file://' + filename)
        elif self._playing is None:
            return
        else:
            logging.debug('continue audio')

        self._player.set_state(Gst.State.PLAYING)
        self._playing = True

    def pause(self):
        if self._playing is not None:
            logging.debug('pause audio')
            self._player.set_state(Gst.State.PAUSED)
            self._playing = False

    def stop(self):
        self._player.set_state(Gst.State.NULL)

    def _gstmessage_cb(self, bus, message):
        message_type = message.type

        if message_type in (Gst.MessageType.EOS, Gst.MessageType.ERROR):
            self._player.set_state(Gst.State.NULL)
            self._playing = None
            logging.debug('audio stoped with type %d' % message_type)
            self.emit('play_finished')
