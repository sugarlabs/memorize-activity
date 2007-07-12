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

import rsvg
import re
import svglabel
import gtk
import gobject
import os

class Score(svglabel.SvgLabel):
    
    selected_color = "#818286"
    default_color = "#4c4d4f"
    status = False
    
    def __init__(self, fill_color, stroke_color, pixbuf= None, pixbuf_sel = None,status= False):
        filename = os.path.join(os.path.dirname(__file__), "images/score.svg")
        self.pixbuf_un = pixbuf
        self.pixbuf_sel = pixbuf_sel
        self.status = status
        if self.pixbuf_un == None:
            self.pixbuf_un = svglabel.SvgLabel(filename, fill_color, stroke_color, False, self.default_color).get_pixbuf()
        if self.pixbuf_sel == None:
            self.pixbuf_sel = svglabel.SvgLabel(filename, fill_color, stroke_color, False, self.selected_color).get_pixbuf()
        if status:
            self.pixbuf = self.pixbuf_sel
        else:
            self.pixbuf = self.pixbuf_un
            
        svglabel.SvgLabel.__init__(self, filename, fill_color, stroke_color, self.pixbuf, self.default_color, 35, 35)     
        self.set_selected(status)
        
    def set_selected(self, status):
        self.status = status
        if status:
            self.pixbuf = self.pixbuf_sel
            self.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse(self.selected_color))
        else:
            self.pixbuf = self.pixbuf_un
            self.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse(self.default_color))
        self.queue_draw()     
        
    def get_pixbuf_un(self):
        return self.pixbuf_un
    
    def get_pixbuf_sel(self):
        return self.pixbuf_sel
        
