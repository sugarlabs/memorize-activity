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
from gobject import SIGNAL_RUN_FIRST, TYPE_PYOBJECT
  
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toggletoolbutton import ToggleToolButton
from sugar.graphics.toolcombobox import ToolComboBox
from sugar.graphics.objectchooser import ObjectChooser

class CreateToolbar(gtk.Toolbar):
    __gtype_name__ = 'CreateToolbar'

    __gsignals__ = {
        'create_new_game': (SIGNAL_RUN_FIRST, None, []), 
        'create_load_game': (SIGNAL_RUN_FIRST, None, [TYPE_PYOBJECT]), 
        'create_save_game': (SIGNAL_RUN_FIRST, None, 3 * [TYPE_PYOBJECT]), 
        'create_equal_pairs': (SIGNAL_RUN_FIRST, None, [TYPE_PYOBJECT]), 
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
        self._new_button.set_tooltip(_('New game'))
        self._new_button.connect('clicked', self._new_game_bt)
        self._add_widget(self._new_button)
        
        # Load Button
        load_icon = os.path.join(os.path.dirname(__file__), "images/game-load.svg")
        load_image = gtk.Image()
        load_image.set_from_file(load_icon)
        self._load_button = ToolButton()
        self._load_button.set_icon_widget(load_image)
        self._load_button.set_tooltip(_('Load game'))
        self._load_button.connect('clicked', self._load_game)
        self._add_widget(self._load_button)
            
        # Save Button
        save_icon = os.path.join(os.path.dirname(__file__), "images/game-save.svg")
        save_image = gtk.Image()
        save_image.set_from_file(save_icon)
        self._save_button = ToolButton()
        self._save_button.set_icon_widget(save_image)
        self._save_button.set_tooltip(_('Save game'))
        self._save_button.connect('clicked', self._save_game_bt)
        self._save_button.set_sensitive(False)
        self._add_widget(self._save_button)
    
        # Separator
        separator2 = gtk.SeparatorToolItem()
        separator2.set_draw(True)
        self.insert(separator2, -1)
        
        self._add_widget(gtk.Label(_('Game name') + ': '))
        self.game_name_entry = gtk.Entry()
        self._add_widget(self.game_name_entry) 
        
        self._equal_pairs = gtk.CheckButton(_('Equal pairs'))   
        self._add_widget(self._equal_pairs)
        self._equal_pairs.connect('toggled', self._emit_equal_pairs)
                
        self._grouped_icon1 = os.path.join(os.path.dirname(__file__), "images/equal_pairs1.svg")
        self._grouped_icon2 = os.path.join(os.path.dirname(__file__), "images/equal_pairs2.svg")
        self._grouped_image1 = gtk.Image()
        self._grouped_image2 = gtk.Image()
        self._grouped_image1.set_from_file(self._grouped_icon1)
        self._grouped_image2.set_from_file(self._grouped_icon2)
        self._grouped = ToggleToolButton()
        self._grouped.set_icon_widget(self._grouped_image1)
        self._grouped.set_tooltip(_('Click for grouped game'))
        self._grouped.connect('toggled', self._grouped_cb)
        self._add_widget(self._grouped)
        
    def _add_widget(self, widget, expand=False):
        tool_item = gtk.ToolItem()
        tool_item.set_expand(expand)
        tool_item.add(widget)
        widget.show()
        self.insert(tool_item, -1)
        tool_item.show()
        
    def _game_changed_cb(self, combobox, game_name):
        self.game_name_entry.set_text(game_name)
        self.emit('create_load_game', game_name)
  
    def _load_game(self, button):
        chooser = ObjectChooser(_('Choose memorize game'), None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        jobject = ''
        try:
            result = chooser.run()
            if result == gtk.RESPONSE_ACCEPT:
                logging.debug('ObjectChooser: %r' % chooser.get_selected_object())
                jobject = chooser.get_selected_object()
                if not jobject or  not jobject.file_path:
                    return
        finally:
            chooser.destroy()
            del chooser
            
        if jobject and jobject.file_path:    
            self.emit('create_load_game', jobject.file_path)
            self._save_button.set_sensitive(False)
        
    def _new_game_bt(self, button):
        self.game_name_entry.set_text('')
        self._equal_pairs.set_active(False)
        self._grouped.set_active(False)
        self.emit('create_new_game')
        self._new_button.set_sensitive(False)
        self._save_button.set_sensitive(False)

    def _save_game_bt(self, button):
        self.emit('create_save_game', self.game_name_entry.get_text(), self._equal_pairs.get_active(), self._grouped.get_active())
        self._save_button.set_sensitive(False)
        
    def _emit_equal_pairs(self, checkbutton):
        self.emit('create_equal_pairs', checkbutton.get_active())
        self._save_button.set_sensitive(True)
        
    def _grouped_cb(self, widget):
        self._save_button.set_sensitive(True)
        if self._grouped.get_active():
            self._grouped.set_icon_widget(self._grouped_image2)
            self._grouped_image2.show()
            self._grouped.set_tooltip(_('Click for ungrouped game'))
        else:
            self._grouped.set_icon_widget(self._grouped_image1)
            self._grouped_image1.show()
            self._grouped.set_tooltip(_('Click for grouped game'))
    
    def update_create_toolbar(self, widget, game_name, equal_pairs, grouped):        
        self.game_name_entry.set_text(game_name)
        self._equal_pairs.set_active(equal_pairs == 'True')
        self._grouped.set_active(grouped == '1')
        
    def update_buttons_status(self, widget, new, save):
        self._new_button.set_sensitive(new)
        self._save_button.set_sensitive(save)
        