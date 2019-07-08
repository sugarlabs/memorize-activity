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

from sugar3.graphics.combobox import ComboBox

import voice


class Voices(ComboBox):
    def __init__(self, face, speech, **kwargs):
        ComboBox.__init__(self, **kwargs)

        self.face = face

        voices = voice.allVoices(speech)
        voicenames = voices.keys()
        voicenames.sort()

        for name in voicenames:
            self.append_item(voices[name], name)

        self.select(voice.defaultVoice(speech))

        self.connect('changed', self._changed_cb)

    def _changed_cb(self, widget):
        self.face.status.voice = widget.props.value
        self.face.say_notification(self.face.status.voice.friendlyname)

    def resume(self, value):
        try:
            self.handler_block_by_func(self._changed_cb)
            self.select_by_lang(value)
            self.face.status.voice = self.props.value
        finally:
            self.handler_unblock_by_func(self._changed_cb)

    def select(self, id=None, name=None):
        if id is not None:
            column = 0
            value = id
        elif name is not None:
            column = 1
            value = name
        else:
            return

        for i, item in enumerate(self.get_model()):
            if item[column] != value:
                continue
            self.set_active(i)
            break

    def select_by_lang(self, lang):
        for i, item in enumerate(self.get_model()):
            if item[0].language != lang:
                continue
            self.set_active(i)
            break
