#! /usr/bin/env python
#
#	Copyright (C) 2006, 2007, One Laptop Per Child
#
#	This program is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; either version 2 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program; if not, write to the Free Software
#	Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

import gtk
import svgcard
import gobject
import logging

_logger = logging.getLogger('memorize-activity')

class CardList(gtk.EventBox):
		
	__gsignals__ = {
		'pair-selected': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT]), 
	}
	
	def __init__(self):
		gtk.EventBox.__init__(self)

		self.pairs = []
		self.current_pair = None
		
		self.set_size_request(450, 150)		
		self.vbox = gtk.VBox(False)		
		
		fill_box = gtk.EventBox()
		fill_box.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#000000'))
		fill_box.show()
		self.vbox.pack_end(fill_box, True, True)
				   
		scroll = gtk.ScrolledWindow()
		#scroll.props.shadow_type = gtk.SHADOW_NONE		   
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		scroll.add_with_viewport(self.vbox)
		scroll.set_border_width(0)
		#scroll.get_child().set_property('shadow-type', gtk.SHADOW_NONE)
		scroll.get_child().modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#000000'))
		self.add(scroll)
		self.add_pair(self, '')
		self.pairs[0].set_selected(True)
		self.current_pair = self.pairs[0]
		self.show()
	
	def add_pair(self, widget, text):
		pair = Pair(text, text)
		self.vbox.pack_end(pair, False, True)
		self.pairs.append(pair)
		pair.connect('pair-selected',self.set_selected)
		pair.connect('pair-closed',self.rem_pair)
		self.show_all()
			
	def rem_pair(self, widget, event):
		self.vbox.remove(widget)		
		del self.pairs[widget]
	
	def set_selected(self, widget, event):
		if self.current_pair <> None:
			self.old = self.current_pair
			self.old.set_selected(False)
		self.current_pair = widget 
		widget.set_selected(True)
		self.emit('pair-selected',self.current_pair.get_text() )
		
	def update_selected(self, widget, newtext):
		self.current_pair.change_text(newtext)
		
class Pair(gtk.EventBox):
	
	__gsignals__ = {
		'pair-selected': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT]), 
		'pair-closed': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT]), 
	}
	
	def __init__(self, text1, text2 = None):
		gtk.EventBox.__init__(self)
		self.bg_color = '#000000'
		if text2 == None:
			self.text2 = text1
		else: 
			self.text2 = text2
		self.text1 = text1
		
		close_button = gtk.Button('X')
		close_button.connect('button-press-event', self.emit_close)
		table = gtk.Table()
		table.connect('button-press-event',self.emit_selected)
		table.set_col_spacings(5)
		table.set_border_width(10)
		self.bcard1 = svgcard.SvgCard(-1, {'front_text':{'card_text':text1, 'text_color':'#ffffff'}, 'front_border':{'fill_color':'#4c4d4f', 'stroke_color':'#ffffff', 'opacity':'1'}}, {}, None, 184, 1, self.bg_color)
		self.bcard2 = svgcard.SvgCard(-1, {'front_text':{'card_text':text2, 'text_color':'#ffffff'}, 'front_border':{'fill_color':'#4c4d4f', 'stroke_color':'#ffffff', 'opacity':'1'}}, {}, None, 184, 1, self.bg_color)
		self.bcard1.flip()
		self.bcard2.flip()
		
		table.attach(self.bcard1, 0, 1, 0, 8)
		table.attach(self.bcard2, 1, 2, 0, 8)
		table.attach(close_button, 2, 3, 0, 1, gtk.FILL, gtk.FILL)
		
		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.bg_color))
		self.add(table)
		self.show_all()

	def emit_selected(self, widget, event):
		self.emit('pair-selected',self)

	def emit_close(self, widget, event):
		self.emit('pair-closed',self)

	def set_selected(self, status):
		if not status:
			self.bg_color = '#000000'
		else:
			self.bg_color = '#b2b3b7'
			
		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.bg_color))
		self.bcard1.set_background(self.bg_color)
		self.bcard2.set_background(self.bg_color)
		
	def change_text(self, newtext):
		self.bcard1.change_text(newtext)
		self.bcard2.change_text(newtext)
	
	def get_text(self):
		return self.bcard1.get_text()