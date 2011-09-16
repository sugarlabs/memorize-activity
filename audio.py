#    Copyright (C) 2006, 2007, 2008 One Laptop Per Child
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

import gst
import logging

_logger = logging.getLogger('memorize-activity')


class Audio(object):
    def __init__(self):
        self._player = gst.element_factory_make('playbin', 'player')
        fakesink = gst.element_factory_make('fakesink', 'my-fakesink')
        self._player.set_property('video-sink', fakesink)
        self._playing = None

        bus = self._player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._gstmessage_cb)

    def play(self, filename=None):
        if filename:
            _logger.debug('play audio %s' % filename)
            self._player.set_property('uri', 'file://' + filename)
            self._player.set_state(gst.STATE_NULL)
        elif self._playing == None:
            return
        else:
            _logger.debug('continue audio')

        self._player.set_state(gst.STATE_PLAYING)
        self._playing = True

    def pause(self):
        if self._playing != None:
            _logger.debug('pause audio')
            self._player.set_state(gst.STATE_PAUSED)
            self._playing = False

    def stop(self):
        self._player.set_state(gst.STATE_NULL)

    def _gstmessage_cb(self, bus, message):
        message_type = message.type

        if message_type in (gst.MESSAGE_EOS, gst.MESSAGE_ERROR):
            self._player.set_state(gst.STATE_NULL)
            self._playing = None
            _logger.debug('audio stoped with type %d' % message_type)
