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
from gettext import gettext as _

import gtk
import os
    
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.combobox import ComboBox

class CreateToolbar(gtk.Toolbar):
    __gtype_name__ = 'CreateToolbar'

    def __init__(self, activity):
        gtk.Toolbar.__init__(self)
        self.activity = activity
        self._lock = True
        
        # Reset Button
        new_icon = os.path.join(os.path.dirname(__file__), "images/new.svg")
        new_image = gtk.Image()
        new_image.set_from_file(new_icon)
        self._reset_button = gtk.ToolButton(new_image)
        #self._reset_button.set_image(new_image)
        #self._reset_button.connect('clicked', self._game_changed_cb)
        self._add_widget(self._reset_button)
        
        # Separator
        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)
        
        self._add_widget(gtk.Label('Game name: '))
        # Change game combobox        
        self.games = os.listdir(os.path.join(os.path.dirname(__file__), 'games'))
        self.games.sort()
        self._game_combo = gtk.ComboBoxEntry()
        for i, f in enumerate(self.games):
            self._game_combo.append_text(f)
            if f == 'numbers':
                self._game_combo.set_active(i)
        #self._game_combo.connect('changed', self._game_changed_cb)
        self._add_widget(self._game_combo)
    
        # Separator
        separator2 = gtk.SeparatorToolItem()
        separator2.set_draw(True)
        self.insert(separator2, -1)
                
        self._add_widget(gtk.CheckButton('Equal pairs'))

        # Separator
        separator2 = gtk.SeparatorToolItem()
        separator2.set_draw(True)
        self.insert(separator2, -1)
                
        self._add_widget(gtk.CheckButton('Grouped'))
                
    def _add_widget(self, widget, expand=False):
        tool_item = gtk.ToolItem()
        tool_item.set_expand(expand)
        tool_item.add(widget)
        widget.show()
        self.insert(tool_item, -1)
        tool_item.show()