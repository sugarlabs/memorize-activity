# Copyright (C) 2009, Aleksey Lim
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
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
from gi.repository import GObject

import logging
logger = logging.getLogger('speak')

PITCH_MIN = 0
PITCH_MAX = 200
RATE_MIN = 0
RATE_MAX = 200


class BaseAudioGrab(GObject.GObject):
    __gsignals__ = {}

    def __init__(self):
        GObject.GObject.__init__(self)
        self.pipeline = None

    def restart_sound_device(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop_sound_device(self):
        if self.pipeline is None:
            return

        self.pipeline.set_state(Gst.State.NULL)

        self.pipeline = None

    def make_pipeline(self):
        if self.pipeline is not None:
            self.stop_sound_device()
            del self.pipeline

        # build a pipeline that makes speech
        # and sends it to only the audio output
        cmd = 'espeak name=espeak ! autoaudiosink'
        self.pipeline = Gst.parse_launch(cmd)


class AudioGrab(BaseAudioGrab):
    def speak(self, status, text):
        self.make_pipeline()
        src = self.pipeline.get_by_name('espeak')

        pitch = int(status.pitch) - 100
        rate = int(status.rate) - 100

        logger.debug('pitch=%d rate=%d voice=%s text=%s' % (pitch, rate,
                                                            status.voice.name,
                                                            text))

        src.props.pitch = pitch
        src.props.rate = rate
        src.props.voice = status.voice.name
        src.props.text = text

        self.restart_sound_device()


def voices():
    out = []

    for i in Gst.ElementFactory.make('espeak', 'espeak').props.voices:
        name, language, dialect = i
        if name in ('en-rhotic', 'english_rp', 'english_wmids'):
            # these voices don't produce sound
            continue
        out.append((language, name, dialect))

    return out
