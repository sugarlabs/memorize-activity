#! /usr/bin/env python
#
#    Copyright (C) 2007, One Laptop Per Child
#
#    Muriel de Souza Godoi - muriel@laptop.org
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

import pango
import svglabel
import os
from score import Score

class PlayerScoreboard(gtk.EventBox):    
    
    def __init__(self, nick, fill_color, stroke_color,score = 0):
        gtk.EventBox.__init__(self)
        
        self.default_color = '#4c4d4f'
        self.selected_color = '#818286'
        self.current_color = '#4c4d4f'
        self.status = False
        
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        
        # Set table
        self.table = gtk.Table(2, 3, True)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.current_color))
        self.table.set_row_spacings(0)
        self.table.set_col_spacings(5)
        self.table.set_border_width(10)
               
        self.scores = []
        self.current_x = 1
        self.current_y = 1
        status = False       
        
        # Set buddy icon
        self.xo_buddy = os.path.join(os.path.dirname(__file__), "images/stock-buddy.svg")
        self.icon = svglabel.SvgLabel(self.xo_buddy, fill_color, stroke_color, False, self.current_color, 45, 55)      
        
        # Set waiting buddy icon
        self.waiting_icon = svglabel.SvgLabel(self.xo_buddy, self.default_color, '#ffffff', False, self.current_color, 45, 55)
        
        # Cache the score icon
        score_label = Score(fill_color, stroke_color)
        self.score_pixbuf_unsel = score_label.get_pixbuf()
        self.score_pixbuf_sel = score_label.get_pixbuf_sel()
        
        # Set nick label
        self.nick = gtk.Label(nick)
        self.nick.modify_font(pango.FontDescription("12"))
        self.nick.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
        self.nick.set_alignment(0, 0.5)
        
        # Set message label
        self.msg = gtk.Label('Waiting for next game...')
        self.msg.modify_font(pango.FontDescription("12"))
        self.msg.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
        self.msg.set_alignment(0, 0.5)
        
        self.add(self.table)
        self.table.attach(self.icon, 0, 1, 0, 1)
        self.table.attach(self.nick, 1, 7, 0, 1)
        
        if score <> 0:
            for i in range(score):
                self.increase_score()
                 
    def increase_score(self):
        new_score = Score(self.fill_color, self.stroke_color, self.score_pixbuf_sel, self.score_pixbuf_unsel,self.status)
        self.scores.append(new_score)
        new_score.show()
        self.table.attach(new_score, self.current_x , self.current_x+1, self.current_y, self.current_y+1)
        self.current_x += 1
        if self.current_x == 7:
            self.current_x = 1
            self.current_y += 1
        self.queue_draw()
            
    def set_selected(self, sel):
        self.status = sel
        if sel:
            self.current_color = self.selected_color
        else:
            self.current_color = self.default_color
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.current_color))
        self.icon.set_background(self.current_color)
        for score in self.scores:
            score.set_selected(sel)
        self.queue_draw()

    def reset(self):
        for score in self.scores:
            self.table.remove(score)
        self.current_x = 1
        self.current_y = 1
        del self.scores
        self.scores = []
        self.queue_draw()
        
    def set_wait_mode(self,status):
        if status:
            self.table.remove(self.icon)
            self.table.attach(self.waiting_icon, 0, 1, 0, 1)
            if len(self.scores) == 0:
                self.table.attach(self.msg, 1, 7, 1, 2)
        else:
            self.table.remove(self.waiting_icon)
            self.table.attach(self.icon, 0, 1, 0, 1)
            self.table.remove(self.msg)
            if len(self.scores) == 0:
                self.table.remove(self.msg)
        self.queue_draw()
        