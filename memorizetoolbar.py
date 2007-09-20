#! /usr/bin/env python
#
#    Copyright (C) 2006, 2007, One Laptop Per Child
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

import logging

import gtk
import os

from gettext import gettext as _
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toolcombobox import ToolComboBox


class MemorizeToolbar(gtk.Toolbar):
    __gtype_name__ = 'MemoryToolbar'
    
    standard_game_names = ["addition", "capitals", "drumgit", "letters", "numbers", "phonemes"]
    translated_game_names = [_("addition"), _("capitals"), _("drumgit"), _("letters"), _("numbers"), _("phonemes")]

    def __init__(self, activity):
        gtk.Toolbar.__init__(self)
        self.activity = activity
        self._lock = True
        
        
        # Reset Button
        self._reset_button = ToolButton('insert-image')
        self._reset_button.connect('clicked', self._game_changed_cb)
        self._reset_button.set_tooltip(_('Restart Game'))
        self.insert(self._reset_button, -1)
        self._reset_button.show()
        
        # Separator
        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)

        # Change game combobox        
        self.games = os.listdir(os.path.join(os.path.dirname(__file__), 'games'))
        self.games.sort()
        self._game_combo = ToolComboBox()
        for i, f in enumerate(self.games):
            if f in self.standard_game_names:
                f = _(f)
            self._game_combo.combo.append_item(i, f)
        self._game_combo.combo.connect('changed', self._game_changed_cb)
        self._add_widget(self._game_combo)
        
        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)
        self._lock = False
        
        # Change size combobox
        self._size_combo = ToolComboBox()
        self._sizes = ['4 X 4', '5 X 5', '6 X 6']
        for i, f in enumerate(self._sizes):
            self._size_combo.combo.append_item(i, f)
        self._size_combo.combo.connect('changed', self._game_changed_cb)
        self._add_widget(self._size_combo)
    
    def _add_widget(self, widget, expand=False):
        tool_item = gtk.ToolItem()
        tool_item.set_expand(expand)
        tool_item.add(widget)
        widget.show()
        self.insert(tool_item, -1)
        tool_item.show()
        
    def _game_changed_cb(self, combobox):
        if not self._lock:
            game_name = self.games[self._game_combo.combo.get_active()]
            game_size = int(self._sizes[self._size_combo.combo.get_active()][0])
            if game_name in self.translated_game_names:
                index = self.translated_game_names.index(game_name)
                game_name = self.standard_game_names[index]
            self.activity.change_game(game_name, game_size)
        
    def update_toolbar(self, widget, data, grid):
        game = data.get('name')
        size = data.get('size')
        self._lock = True
        game_index = self.games.index(game)
        self._game_combo.combo.set_active(game_index)
        size_index = self._sizes.index(size+' X '+size)
        self._size_combo.combo.set_active(int(size_index))
        self._lock = False
