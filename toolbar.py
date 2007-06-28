# Copyright (C) 2007, Simon Schampijer
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

from gettext import gettext as _
import logging

import gtk

from sugar.graphics.combobox import ComboBox
from sugar.graphics.toolbutton import ToolButton


class PlayToolbar(gtk.Toolbar):
    def __init__(self, activity): 
        gtk.Toolbar.__init__(self)

        self._activity = activity

        self._image = ToolButton('go-previous')
        self._image_id = self._image.connect('clicked', self._back_cb)
        self.insert(self._image, -1)
        self._image.show()

        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)

        self._num_players_combo = ComboBox()
        self._num_players = ['1', '2', '3', '4', '5', '6', '7', '8']
        self._num_players_combo.connect('changed', self._num_players_changed_cb)
        for i, s in enumerate(self._num_players):
            self._num_players_combo.append_item(i, s, None)
            if s == '1':
                self._num_players_combo.set_active(i)
        self._add_widget(self._num_players_combo)

        #self.close = ToolButton('window-close')
        #self.close.connect('clicked', self._close_clicked_cb)
        #self.insert(self.close, -1)
        #self.close.show()

    #def _close_clicked_cb(self, button):
    #    self._activity.close()        

    def _add_widget(self, widget, expand=False):
        tool_item = gtk.ToolItem()
        tool_item.set_expand(expand)

        tool_item.add(widget)
        widget.show()

        self.insert(tool_item, -1)
        tool_item.show()
        
    def _num_players_changed_cb(self, num_players_combo):
        logging.debug('num_players=' + self._num_players[self._num_players_combo.get_active()] )
        
    def _back_cb(self, button):
        pass

