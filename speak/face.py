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
import sugar3.speech as Speech

import eye
import mouth
import voice

from gi.repository import Gtk

logger = logging.getLogger('speak')

FACE_PAD = style.GRID_CELL_SIZE


class Status:
    def __init__(self):
        self.speech= Speech.SpeechManager()
        self.voice = voice.defaultVoice()
        self.pitch = self.speech.MAX_PITCH
        self.rate = self.speech.MAX_RATE

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

    def clone(self):
        new = Status()
        new.voice = self.voice
        new.pitch = self.pitch
        new.rate = self.rate
        new.eyes = self.eyes
        new.mouth = self.mouth
        return new


class View(Gtk.EventBox):
    def __init__(self, fill_color=style.COLOR_BUTTON_GREY):
        Gtk.EventBox.__init__(self)

        self.speech= Speech.SpeechManager()
        self.status = Status()
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

        self._peding = None
        self.connect('map', self.__map_cb)

        self.update()

    def __map_cb(self, widget):
        if self._peding:
            self.update(self._peding)
            self._peding = None

    def look_ahead(self):
        pass

    def look_at(self, x, y):
        pass

    def update(self, status=None):
        if not status:
            status = self.status
        else:
            if not self.get_mapped():
                self._peding = status
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
        self.speech.say_text(self._peding or self.status, something)

    def say_notification(self, something):
        status = (self._peding or self.status).clone()
        status.voice = voice.defaultVoice()
        self.speech.say_text(status, something)

    def shut_up(self):
        self.speech.stop()

    def _size_allocate_cb(self, widget, allocation):
        self._mouthbox.set_size_request(-1, int(allocation.height / 2.5))
