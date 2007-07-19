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

class CreateTable(gtk.EventBox):
  
    __gsignals__ = {
        'card-flipped': (gobject.SIGNAL_RUN_FIRST, None, [int, gobject.TYPE_PYOBJECT]), 
        'card-highlighted': (gobject.SIGNAL_RUN_FIRST, None, [int, gobject.TYPE_PYOBJECT]), 
        }

    TARGET_TYPE_TEXT = 80
    TARGET_TYPE_JPG = 81
    TARGET_TYPE_AUDIO = 82
    mime = [ ( "text/plain", 0, TARGET_TYPE_TEXT ), ( "image/x-jpg", 0, TARGET_TYPE_JPG ),
             ( "image/x-audio", 0, TARGET_TYPE_AUDIO ) ]
    
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

    def make_table(self, numpairs):
        ylen=numpairs
        xlen=4
        self.size = int(math.ceil(math.sqrt(xlen*ylen)))
        self.card_size = self.get_card_size(self.size)
        print self.card_size
        props={}
        props['front_border'] = {'opacity':'1'}
        props['front_h_border'] ={'opacity':'1'}
        props['front_text']= {'card_text':'', 'card_line1':'', 'card_line2':'', 'card_line3':'', 'card_line4':''}
        buffer_card = svgcard.SvgCard(-1, {'front_border':{'opacity':'0'}, 'front_h_border':{'opacity':'0.5'},
                                             'back_text':{'card_text':''}}, {}, None, self.card_size)
        
        jpg = None
        x=y=0
        x2=y2=1
        while y < ylen:            
            while x < xlen:
                print '[%d %d %d %d]'%(x,x2,y,y2)
                card = svgcard.SvgCard(id, props, buffer_card.get_cache(), jpg, self.card_size)                
                card.connect('drag_data_received', self.receiveCallback)
                card.drag_dest_set(gtk.DEST_DEFAULT_MOTION |
                                gtk.DEST_DEFAULT_HIGHLIGHT |
                                gtk.DEST_DEFAULT_DROP,
                                   self.mime, gtk.gdk.ACTION_COPY)                
                self.table.attach(card, x, x2, y, y2)
                x+=1
                x2+=1
            x=0
            x2=1
            y+=1
            y2+=1


    def receiveCallback(self, widget, context, x, y, selection, targetType,
                        time):
        print 'receive'
        if targetType == self.TARGET_TYPE_JPG:            
            print 'Img: selection.data: %s x=%f y=%f'%(selection.data, x, y)
            widget.jpeg = selection.data
            widget.flip()

        if targetType == self.TARGET_TYPE_TEXT:            
            print 'Char: selection.data: %s x=%f y=%f'%(selection.data, x, y)
            widget.props['front_text']['card_text'] = selection.data
            widget.flip()

        if targetType == self.TARGET_TYPE_AUDIO:            
            print 'Audio: selection.data: %s x=%f y=%f'%(selection.data, x, y)
            widget.jpeg = 'ohr.jpg'
            widget.flip()

    
    def get_card_size(self, size_table):
        x = (780 - (11*size_table))/size_table
        return x
