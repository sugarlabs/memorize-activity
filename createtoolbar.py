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
import gobject
  
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toolcombobox import ToolComboBox

class CreateToolbar(gtk.Toolbar):
    __gtype_name__ = 'CreateToolbar'

    __gsignals__ = {
        'create_new_game': (gobject.SIGNAL_RUN_FIRST, None, []),
        'create_load_game': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT]), 
        'create_save_game': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT]), 
    }
    
    def __init__(self, activity):
        gtk.Toolbar.__init__(self)
        self.activity = activity
        self._lock = True
        
        # New Button
        new_icon = os.path.join(os.path.dirname(__file__), "images/game-new.svg")
        new_image = gtk.Image()
        new_image.set_from_file(new_icon)
        self._new_button = ToolButton()
        self._new_button.set_icon_widget(new_image)
        self._new_button.set_tooltip(_('New game set'))
        self._new_button.connect('clicked', self._new_game_bt)
        self._add_widget(self._new_button)
        
        # Load Button
        load_icon = os.path.join(os.path.dirname(__file__), "images/game-load.svg")
        load_image = gtk.Image()
        load_image.set_from_file(load_icon)
        self._load_button = ToolButton()
        self._load_button.set_icon_widget(load_image)
        self._load_button.set_tooltip(_('Load game set'))
        self._load_button.connect('enter-notify-event', self._drop_palette)
        self._add_widget(self._load_button)
        self.games = os.listdir(os.path.join(os.path.dirname(__file__), 'games'))
        self.games.sort()
        palette = self._load_button.get_palette()
        for game in self.games:
            menu_item = gtk.MenuItem(game)
            menu_item.connect('activate', self._game_changed_cb, game)
            palette.menu.prepend(menu_item)
            menu_item.show()
            
        # Save Button
        save_icon = os.path.join(os.path.dirname(__file__), "images/game-save.svg")
        save_image = gtk.Image()
        save_image.set_from_file(save_icon)
        self._save_button = ToolButton()
        self._save_button.set_icon_widget(save_image)
        self._save_button.set_tooltip(_('Save game set'))
        self._save_button.connect('clicked', self._save_game_bt)
        self._add_widget(self._save_button)
    
        # Separator
        separator2 = gtk.SeparatorToolItem()
        separator2.set_draw(True)
        self.insert(separator2, -1)
        
        self._add_widget(gtk.Label(_('Game name: ')))
        self.game_name_entry = gtk.Entry()
        self._add_widget(self.game_name_entry) 
               
        self._add_widget(gtk.CheckButton('Equal pairs'))
                
        self._add_widget(gtk.CheckButton('Grouped'))

                
    def _add_widget(self, widget, expand=False):
        tool_item = gtk.ToolItem()
        tool_item.set_expand(expand)
        tool_item.add(widget)
        widget.show()
        self.insert(tool_item, -1)
        tool_item.show()
        
    def _game_changed_cb(self, combobox, game_name):
        self.game_name_entry.set_text(game_name)
        self.emit('create_load_game',game_name)
  
    def _drop_palette(self, button):
        button.get_palette().popdown(False)
        
    def _new_game_bt(self, button):
        self.game_name_entry.set_text('')
        self.emit('create_new_game')

    def _save_game_bt(self, button):
        self.emit('create_save_game',self.game_name_entry.get_text())        