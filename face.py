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
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from gi.repository import Gdk
from gi.repository import Gtk

import logging

from sugar3.graphics import style

import speak.face


class Face(Gtk.EventBox):
    def __init__(self):
        Gtk.EventBox.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL, style.COLOR_BLACK.get_gdk_color())

        self.face = speak.face.View(style.Color('#4b4c4e'))
        self.face.set_border_width(style.DEFAULT_SPACING)
        self.add(self.face)
        self.show_all()

        self.set_app_paintable(True)
        self.connect('unrealize', self._unrealize_cb)

    def _unrealize_cb(self, widget):
        self.face.shut_up()


def look_at():
    display = Gdk.Display.get_default()
    screen_, x, y, modifiers_ = display.get_pointer()

    for i in _cache:
        if i.get_parent():
            i.face.look_at(x, y)


def acquire():
    face = None

    for i in _cache:
        i.face.shut_up()
        if not i.get_parent():
            face = i

    if not face:
        face = Face()
        _cache.append(face)
        logging.debug('face._cache size %s' % len(_cache))

    return face


_cache = []
