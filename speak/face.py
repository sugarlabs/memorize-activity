# Speak.activity
# A simple front end to the espeak text-to-speech engine on the XO laptop
# http://wiki.laptop.org/go/Speak
#
# Copyright (C) 2008  Joshua Minor
# This file is part of Speak.activity
#
# Parts of Speak.activity are based on code from Measure.activity
# Copyright (C) 2007  Arjun Sarwal - arjun@laptop.org
#
#     Speak.activity is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Speak.activity is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Speak.activity.  If not, see <http://www.gnu.org/licenses/>.


import logging
import json

import sugar3.graphics.style as style

import eye
import mouth
import voice

from gi.repository import Gtk

logger = logging.getLogger('speak')

FACE_PAD = style.GRID_CELL_SIZE


class Status:

    def __init__(self, speech):
        self.speech = speech
        self.voice = voice.defaultVoice(speech)
        self.pitch = self.speech.get_pitch()
        self.rate = self.speech.get_rate()

        self.eyes = [eye.Eye] * 2
        self.mouth = mouth.Mouth

    def serialize(self):
        eyes = {eye.Eye: 1}
        mouths = {mouth.Mouth: 1}

        return json.dumps({
            'voice': {'language': self.voice.language,
                      'name': self.voice.name},
            'pitch': self.pitch,
            'rate': self.rate,
            'eyes': [eyes[i] for i in self.eyes],
            'mouth': mouths[self.mouth]})

    def deserialize(self, buf):
        eyes = {1: eye.Eye}
        mouths = {1: mouth.Mouth}

        data = json.loads(buf)
        self.voice = voice.Voice(data['voice']['language'],
                                 data['voice']['name'])
        self.pitch = data['pitch']
        self.rate = data['rate']
        self.eyes = [eyes[i] for i in data['eyes']]
        self.mouth = mouths[data['mouth']]

        return self

    def clone(self, speech):
        new = Status(speech)
        new.voice = self.voice
        new.pitch = self.pitch
        new.rate = self.rate
        new.eyes = self.eyes
        new.mouth = self.mouth
        return new


class View(Gtk.EventBox):
    def __init__(self, speech, fill_color=style.COLOR_BUTTON_GREY):
        Gtk.EventBox.__init__(self)

        self.speech = speech
        self.status = Status(self.speech)
        self.fill_color = fill_color

        self.connect('size-allocate', self._size_allocate_cb)

        # make an empty box for some eyes
        self._eyes = None
        self._eyebox = Gtk.HBox()
        self._eyebox.show()

        # make an empty box to put the mouth in
        self._mouth = None
        self._mouthbox = Gtk.HBox()
        self._mouthbox.show()

        # layout the screen
        self._box = Gtk.VBox(homogeneous=False)
        self._box.pack_start(self._eyebox, True, True, 0)
        self._box.pack_start(self._mouthbox, False, True, 0)
        self._box.set_border_width(FACE_PAD)
        self.modify_bg(Gtk.StateType.NORMAL, self.fill_color.get_gdk_color())
        self.add(self._box)

        self._pending = None
        self.connect('map', self.__map_cb)

        self.update()

    def __map_cb(self, widget):
        if self._pending:
            self.update(self._pending)
            self._pending = None

    def look_ahead(self):
        pass

    def look_at(self, x, y):
        pass

    def update(self, status=None):
        if not status:
            status = self.status
        else:
            if not self.get_mapped():
                self._pending = status
                return
            self.status = status

        if self._eyes:
            for the in self._eyes:
                self._eyebox.remove(the)
        if self._mouth:
            self._mouthbox.remove(self._mouth)

        self._eyes = []

        for i in status.eyes:
            the = i(self.fill_color)
            self._eyes.append(the)
            self._eyebox.pack_start(the, True, True, FACE_PAD)
            the.show()

        self._mouth = status.mouth(self.speech, self.fill_color)
        self._mouth.show()
        self._mouthbox.add(self._mouth)

    def say(self, something):
        if self._pending is None:
            pitch = int(self.status.pitch)
            rate = int(self.status.rate)
            voice_name = self.status.voice.name
        else:
            pitch = int(self._pending.pitch)
            rate = int(self._pending.rate)
            voice_name = self._pending.voice.name
        all_voices = self.speech.get_all_voices()
        lang_code = None
        for lang, name in all_voices.items():
            if name == voice_name:
                lang_code = lang
        self.speech.say_text(something, pitch, rate, lang_code)

    def say_notification(self, something):
        status = (self._pending or self.status).clone(self.speech)
        status.voice = voice.defaultVoice(self.speech)
        pitch = int(status.pitch)
        rate = int(status.rate)
        voice_name = status.voice.name
        all_voices = self.speech.get_all_voices()
        lang_code = None
        for lang, name in all_voices.items():
            if name == voice_name:
                lang_code = lang
        self.speech.say_text(something, pitch, rate, lang_code)

    def shut_up(self):
        self.speech.stop()

    def _size_allocate_cb(self, widget, allocation):
        self._mouthbox.set_size_request(-1, int(allocation.height / 2.5))
