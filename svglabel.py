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
import rsvg
import cairo
import re

class SvgLabel(gtk.DrawingArea):
    
    filename = ''
    fill_color = ''
    stroke_color = ''
    background_color = ''
    
           
    def __init__(self, filename, fill_color, stroke_color, pixbuf = False, background_color = '', request_x = 45, request_y = 45):
        gtk.DrawingArea.__init__(self)
        self.set_size_request(request_x, request_y)
        self.filename = filename
        self.background_color = background_color
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(background_color))
        if pixbuf:
            self.pixbuf = pixbuf
        else:      
            self.pixbuf = self._read_icon_data(self.filename, self.fill_color, self.stroke_color)
            
        self.connect('expose-event', self._expose_cb)
    
    def _expose_cb(self, widget, event):
        widget.window.draw_pixbuf(None, self.pixbuf, 0, 0, 0, 0)
        return False
        
    def _read_icon_data(self, filename, fill_color, stroke_color):
        icon_file = open(filename, 'r')
        data = icon_file.read()
        icon_file.close()

        if fill_color:
            entity = '<!ENTITY fill_color "%s">' % fill_color
            data = re.sub('<!ENTITY fill_color .*>', entity, data)

        if stroke_color:
            entity = '<!ENTITY stroke_color "%s">' % stroke_color
            data = re.sub('<!ENTITY stroke_color .*>', entity, data)

        self.data_size = len(data)
        return rsvg.Handle(data=data).get_pixbuf()
    
    def set_color(self, fill_color, stroke_color):
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.pixmap = self._read_icon_data(self.filename, self.fill_color, self.stroke_color) 
        self.queue_draw()        
    
    def set_fill_color(self, fill_color):
        self.fill_color = fill_color
        self.pixmap = self._read_icon_data(self.filename, self.fill_color, self.stroke_color)
        self.queue_draw() 
        
    def get_fill_color(self):
        return self.fill_color
    
    def set_stroke_color(self, stroke_color):
        self.stroke_color = stroke_color
        self.pixmap = self._read_icon_data(self.filename, self.fill_color, self.stroke_color)
        self.queue_draw() 
    
    def get_stroke_color(self):
        return self.stroke_color
    
    def get_pixbuf(self):
        return self.pixbuf
    
    def set_pixbuf(self, pixbuf):
        self.pixbuf = pixbuf
        self.queue_draw() 
        
    def set_background(self, background_color):
        self.background_color = background_color
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
        self.queue_draw() 
               
