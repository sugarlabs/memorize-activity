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

import gtk

import logging
_logger = logging.getLogger('memorize-activity')

from sugar.graphics import style

import speak.espeak
import speak.face
import theme


class Face(gtk.EventBox):
    def __init__(self):
        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, style.COLOR_BLACK.get_gdk_color())

        self.face = speak.face.View(style.Color('#4b4c4e'))
        self.face.set_border_width(theme.SVG_PAD)
        self.add(self.face)
        self.show_all()

        self.set_app_paintable(True)
        self.connect('expose-event', self._expose_cb)
        self.connect('unrealize', self._unrealize_cb)

    def _unrealize_cb(self, widget):
        self.face.shut_up()

    def _expose_cb(self, widget, event):
        card = self.parent.parent
        pixbuf = card._read_icon_data('front')
        self.window.draw_pixbuf(None, pixbuf, 0, 0, 0, 0)


def look_at():
    if not speak.espeak.supported:
        return

    display = gtk.gdk.display_get_default()
    screen_, x, y, modifiers_ = display.get_pointer()

    for i in _cache:
        if i.parent:
            i.face.look_at(x, y)


def acquire():
    if not speak.espeak.supported:
        return None

    face = None

    for i in _cache:
        i.face.shut_up()
        if not i.parent:
            face = i

    if not face:
        face = Face()
        _cache.append(face)
        _logger.debug('face._cache size %s' % len(_cache))

    return face

_cache = []
