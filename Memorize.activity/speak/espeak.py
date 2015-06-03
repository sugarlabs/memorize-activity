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

from gi.repository import Gst
from gi.repository import GObject
import subprocess

import logging
logger = logging.getLogger('speak')

supported = True

class BaseAudioGrab(GObject.GObject):
    __gsignals__ = {
        'new-buffer': (GObject.SignalFlags.RUN_FIRST, None, [GObject.TYPE_PYOBJECT])
    }

    def __init__(self):
        GObject.GObject.__init__(self)
        self.pipeline = None
        self.quiet = True

    def restart_sound_device(self):
        self.quiet = False

        self.pipeline.set_state(Gst.State.NULL)
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop_sound_device(self):
        if self.pipeline is None:
            return

        self.pipeline.set_state(Gst.State.NULL)
        # Shut theirs mouths down
        self._new_buffer('')

        self.quiet = True

    def make_pipeline(self, cmd):
        if self.pipeline is not None:
            self.stop_sound_device()
            del self.pipeline

        # build a pipeline that reads the given file
        # and sends it to both the real audio output
        # and a fake one that we use to draw from
        self.pipeline = Gst.parse_launch(cmd)

    def _new_buffer(self, buf):
        if not self.quiet:
            # pass captured audio to anyone who is interested
            self.emit("new-buffer", buf)
        return False

# load proper espeak plugin
try:
    from gi.repository import Gst
    Gst.init([])
    Gst.ElementFactory.make('espeak', None)
    from espeak_gst import AudioGrabGst as AudioGrab
    from espeak_gst import *
    logger.info('use gst-plugins-espeak')
except Exception, e:
    logger.info('disable gst-plugins-espeak: %s' % e)
    if subprocess.call('which espeak', shell=True) == 0:
        from espeak_cmd import AudioGrabCmd as AudioGrab
        from espeak_cmd import *
    else:
        logger.info('disable espeak_cmd')
        supported = False
