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

import gtk
from os.path import join, dirname

from gettext import gettext as _
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toolcombobox import ToolComboBox
from sugar.graphics.objectchooser import ObjectChooser
import logging
from gobject import SIGNAL_RUN_FIRST, TYPE_PYOBJECT

_logger = logging.getLogger('memorize-activity')

class MemorizeToolbar(gtk.Toolbar):
    __gtype_name__ = 'MemoryToolbar'
    
    standard_game_names = ['Load demo games',
                           'addition',
                           'letters',
                           'drumgit'
                           ]
    translated_game_names = [_('Load demo games'),
                             _('addition'),
                             _('letters'),
                             _('drumgit')
                            ]

    __gsignals__ = {
    'game_changed': (SIGNAL_RUN_FIRST, None, 5 * [TYPE_PYOBJECT])
    }
    
    def __init__(self, activity):
        gtk.Toolbar.__init__(self)
        self.activity = activity
        self._lock = True
        self.jobject = None
        
        # Reset Button
        restart_icon = join(dirname(__file__), 'images', 'game-restart.svg')
        restart_image = gtk.Image()
        restart_image.set_from_file(restart_icon)
        self._restart_button = ToolButton()
        self._restart_button.set_icon_widget(restart_image)
        self._restart_button.connect('clicked', self._game_reset_cb)
        self._restart_button.set_tooltip(_('Restart Game'))
        self.insert(self._restart_button, -1)
        self._restart_button.show()
        
        # Load Button
        load_icon = join(dirname(__file__), 'images', 'game-load.svg')
        load_image = gtk.Image()
        load_image.set_from_file(load_icon)
        self._load_button = ToolButton()
        self._load_button.set_icon_widget(load_image)
        self._load_button.set_tooltip(_('Load game'))
        self._load_button.connect('clicked', self._load_game)
        self._add_widget(self._load_button)
        
        # Separator
        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)
        
        # Change size combobox
        self._size_combo = ToolComboBox()
        self._sizes = ['4 X 4', '5 X 5', '6 X 6']
        for i, f in enumerate(self._sizes):
            self._size_combo.combo.append_item(i, f)
        self.size_handle_id = self._size_combo.combo.connect('changed', self._game_size_cb)
        self._add_widget(self._size_combo)
        self._size_combo.combo.set_active(0)
        
        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)
        self._lock = False
    
        # Change demo games combobox        
        self._game_combo = ToolComboBox()
        for i, f in enumerate(self.standard_game_names):
            f = _(f)    
            self._game_combo.combo.append_item(i, f)
        self._game_combo.combo.set_active(0)
        self._game_combo.combo.connect('changed', self._game_changed_cb)
        self._add_widget(self._game_combo)
    
    def _add_widget(self, widget, expand=False):
        tool_item = gtk.ToolItem()
        tool_item.set_expand(expand)
        tool_item.add(widget)
        widget.show()
        self.insert(tool_item, -1)
        tool_item.show()
        
    def _game_reset_cb(self, widget):
        self.emit('game_changed', None, None, 'reset', None, None)
        
    def _load_game(self, button):
        chooser = ObjectChooser(_('Choose memorize game'),
                                 None, 
                                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
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
            title = jobject.metadata['title']
            color = jobject.metadata['icon-color']
            self.emit('game_changed', jobject.file_path, 4, 'file', title, color)
             
            if self.jobject != None:
                self.jobject.destroy()
            self.jobject = jobject
    
    def _game_size_cb(self, widget):
        game_size = int(self._sizes[self._size_combo.combo.get_active()][0])
        self.emit('game_changed', None, game_size, 'size', None, None)
    
    def _game_changed_cb(self, combobox):
        if combobox.get_active() == 0: return
        title = game_name = self.standard_game_names[self._game_combo.combo.get_active()]
        game_size = int(self._sizes[self._size_combo.combo.get_active()][0])
        
        if game_name in self.translated_game_names:
            index = self.translated_game_names.index(game_name)
            game_name = self.standard_game_names[index]
            
        game_file = join(dirname(__file__), 'demos', game_name+'.zip')
        self.emit('game_changed', game_file, game_size, 'demo', title, None)
        self._game_combo.combo.set_active(0)
        
    def update_toolbar(self, widget, data, grid):
        size = data.get('size')
        self._size_combo.combo.handler_block(self.size_handle_id)
        size_index = self._sizes.index(size+' X '+size)
        self._size_combo.combo.set_active(int(size_index))
        self._size_combo.combo.handler_unblock(self.size_handle_id)
