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

import gtk, pygtk
import svgcard
import os
import time
import gobject
import math
import gc

class CardTable(gtk.EventBox):
  
    __gsignals__ = {
        'card-flipped': (gobject.SIGNAL_RUN_FIRST, None, [int, gobject.TYPE_PYOBJECT]), 
        'card-highlighted': (gobject.SIGNAL_RUN_FIRST, None, [int, gobject.TYPE_PYOBJECT]), 
        }

    def __init__(self):
        gtk.EventBox.__init__(self)
        
        # Set table settings
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#000000'))
        self.table = gtk.Table()
        self.table.grab_focus()
        self.table.set_flags(gtk.CAN_FOCUS)
        self.table.set_flags(gtk.CAN_DEFAULT)
        self.table.set_row_spacings(11)
        self.table.set_col_spacings(11)
        self.table.set_border_width(11)
        self.table.set_resize_mode(gtk.RESIZE_IMMEDIATE)
        self.set_property('child', self.table)
        self.fist_load = True
        
    def load_game(self, widget, data, grid):
        self.data = data
        self.cards_data = grid
        self.size = int(math.ceil(math.sqrt(len(grid))))
        self.table.resize(self.size, self.size)
        self.card_size = self.get_card_size(self.size)
        self.cards = {}
        self.cd2id = {}
        self.id2cd = {}
        self.dict = {}
        self.selected_card = [0, 0]
        self.flipped_card = -1
        self.table_positions = {}
        
        # Build the table
        if data['divided']=='1':
            text1 = str(self.data['face1'])
            text2 = str(self.data['face2'])
        else:
            text1 = str(self.data['face'])
            text2 = str(self.data['face'])
        buffer_card_1 = svgcard.SvgCard(-1, {'front_border':{'opacity':'0'}, 'front_h_border':{'opacity':'0.5'}, 'back_text':{'card_text':text1}}, {}, None, self.card_size)
        buffer_card_2 = svgcard.SvgCard(-1, {'front_border':{'opacity':'0'}, 'front_h_border':{'opacity':'0.5'}, 'back_text':{'card_text':text2}}, {}, None, self.card_size)
        
        x = 0
        y = 0
        id = 0
        
        for card in self.cards_data:        
            if card.get('img', None):
                jpg = card['img']
            else:
                jpg = None
            props = {}
            props['front_border'] = {'opacity':'1'}
            props['front_h_border'] ={'opacity':'1'}
            if self.data['align'] == '1': 
                props['front_text']= {'card_text':card.get('char', ''), 'card_line1':'', 'card_line2':'',
                                      'card_line3':'', 'card_line4':''}
            elif self.data['align'] == '2': 
                props['front_text']= {'card_text':'', 'card_line1':card.get('char', ''), 'card_line2':'',
                                      'card_line3':'', 'card_line4':''}
            elif self.data['align'] == '3': 
                props['front_text']= {'card_text':'', 'card_line1':'',
                                      'card_line2':card.get('char', ''), 'card_line3':'', 'card_line4':''}
                    
            if card['ab']== 'a':
                buffer_card = buffer_card_1
            elif card['ab']== 'b':
                buffer_card = buffer_card_2
            
            card = svgcard.SvgCard(id, props, buffer_card.get_cache(), jpg, self.card_size)
            card.connect('enter-notify-event', self.mouse_event, [x, y])
            card.connect("button-press-event", self.flip_card_mouse, id)
            self.table_positions[(x, y)]=1
            self.cd2id[card] = id
            self.id2cd[id] = card
            self.cards[(x, y)] = card
            self.dict[id] = (x, y)            
            self.table.attach(card, x, x+1, y, y+1, gtk.SHRINK, gtk.SHRINK)
            #button = gtk.Button('button')
            #button.show()
            #self.table.attach(button, x, x+1, y, y+1, gtk.SHRINK, gtk.SHRINK)
            x += 1
            if x == self.size:
                x = 0
                y +=1
            id += 1
        self.fist_load = False
        gc.collect()
            
    def change_game(self, widget, data, grid):
        if not self.fist_load:
            for card in self.cards.values():
                self.table.remove(card)
                del card
        self.load_game(None, data, grid)
    
    def get_card_size(self, size_table):
        x = (780 - (11*size_table))/size_table
        return x
        
    def mouse_event(self, widget, event, coord):
        #self.table.grab_focus()
        card = self.cards[coord[0], coord[1]]
        id = self.cd2id.get(card)
        self.emit('card-highlighted', id, True)
        self.selected_card = (coord[0], coord[1])
            
    def key_press_event(self, widget, event):
        #self.table.grab_focus()
        x= self.selected_card[0]
        y= self.selected_card[1]
        
        if event.keyval in (gtk.keysyms.Left, gtk.keysyms.KP_Left,gtk.keysyms.a):
            if self.table_positions.has_key((x-1, y)):
                card = self.cards[x-1, y]
                id = self.cd2id.get(card)
                self.emit('card-highlighted', id, False)
        
        elif event.keyval in (gtk.keysyms.Right, gtk.keysyms.KP_Right,gtk.keysyms.d):
            if self.table_positions.has_key((x+1, y)):
                card = self.cards[x+1, y]
                id = self.cd2id.get(card)
                self.emit('card-highlighted', id, False)
        
        elif event.keyval in (gtk.keysyms.Up, gtk.keysyms.KP_Up,gtk.keysyms.w):
            if self.table_positions.has_key((x, y-1)):
                card = self.cards[x, y-1]
                id = self.cd2id.get(card)
                self.emit('card-highlighted', id, False)
        
        elif event.keyval in (gtk.keysyms.Down, gtk.keysyms.KP_Down,gtk.keysyms.s):
            if self.table_positions.has_key((x, y+1)):
                card = self.cards[x, y+1]
                id = self.cd2id.get(card)
                self.emit('card-highlighted', id, False)
        
        elif event.keyval in (gtk.keysyms.space,gtk.keysyms.KP_Page_Down):
            card = self.cards[x, y]
            self.card_flipped(card)
    
    def flip_card_mouse(self, widget, event, id):
        position = self.dict[id]
        card = self.cards[position]
        self.card_flipped(card)
        
    def card_flipped(self, card):
        if not card.is_flipped():
            id  = self.cd2id[card]
            self.emit('card-flipped', id, False)
            
    def set_border(self, widget, id, stroke_color, fill_color):
        self.id2cd[id].set_border(stroke_color, fill_color)

    def flop_card(self, widget, id):
        self.id2cd.get(id).flop()

    def flip_card(self, widget, id):
        self.id2cd.get(id).flip()
        
    def highlight_card(self, widget, id, status):
        self.selected_card = self.dict.get(id)
        self.id2cd.get(id).set_highlight(status)
        
    def reset(self, widget):        
        for id in self.id2cd.keys():
           self.id2cd[id].reset()
