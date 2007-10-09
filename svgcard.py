#! /usr/bin/env python
#
#	Copyright (C) 2007, One Laptop Per Child
#
#	Muriel de Souza Godoi - muriel@laptop.org
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

import os
import gc
import rsvg
import re
import gtk
import pango
import logging

_logger = logging.getLogger('memorize-activity')

class SvgCard(gtk.DrawingArea):
		
	border_svg = os.path.join(os.path.dirname(__file__), "images/card.svg")

	# Default properties
	default_props = {}
	default_props['back'] = {'fill_color':'#b2b3b7', 'stroke_color':'#b2b3b7', 'opacity':'1'}
	default_props['back_h'] = {'fill_color':'#b2b3b7', 'stroke_color':'#ffffff', 'opacity':'1'}
	default_props['back_text'] = {'text_color':'#c7c8cc'}
	default_props['front'] = {'fill_color':'#4c4d4f', 'stroke_color':'#ffffff', 'opacity':'1'}
	default_props['front_h'] = {'fill_color':'#555555', 'stroke_color':'#888888', 'opacity':'1'}
	default_props['front_text'] = {'text_color':'#ffffff'}
	
	cache = {}
	
	def __init__(self, id, pprops, jpeg, size, align, bg_color='#000000'):
		gtk.DrawingArea.__init__(self)
		self.set_size_request(size, size)
		self.bg_color = bg_color
		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.bg_color))		
		self.flipped = False
		self.flipped_once = False
		self.id = id	  
		self.jpeg = jpeg
		self.show_jpeg = False 
		self.show_text = False 
		self.size = size
		self.align = align
				
		# Views properties
		views = ['back', 'back_h', 'back_text', 'front', 'front_h', 'front_text']
		self.pprops = pprops
		self.props = {}
		for view in views:
			self.props[view] = {}
			self.props[view].update(self.default_props[view])
			self.props[view].update(pprops.get(view, {}))
	
		if len(self.props['back_text'].get('card_text', '')) > 0:
		   	self.back_layout = self.get_text_layout(self.props['back_text']['card_text'], self.size-12)
		   	self.back_layout_position = (self.size -(self.back_layout.get_size()[1]/1000))/2
			self.current_layout = self.back_layout
			self.current_layout_position = self.back_layout_position
			self.current_text_color = self.props['back_text']['text_color']
		   	self.show_text = True
		self.current_face = 'back'
		
		# Set events and listeners
		self.connect('expose-event', self._expose_cb)
		self.set_events(gtk.gdk.ALL_EVENTS_MASK)
		gc.collect()
		self.show()

	def _expose_cb(self, widget, event):
		gc = self.window.new_gc()
		pixbuf = self._read_icon_data(self.current_face)
		self.window.draw_pixbuf(None, pixbuf, 0, 0, 0, 0)
		if self.show_jpeg:
			self.window.draw_pixbuf(None, self.jpeg, 0, 0, 11, 11)
		if self.show_text:
			widget.window.draw_layout(gc, x=6, y=self.current_layout_position, layout=self.current_layout, foreground=gtk.gdk.color_parse(self.current_text_color))
		return False

	def _read_icon_data(self, view):
		dict = self.props[view]
		set  = str(self.size)+dict.get('fill_color')+dict.get('stroke_color')
		if self.cache.has_key(set):
			return self.cache[set]
			
		icon_file = open(self.border_svg, 'r')
		data = icon_file.read()
		icon_file.close()

		# Replace borders parameters
		entity = '<!ENTITY fill_color "%s">' % dict.get('fill_color', '')
		data = re.sub('<!ENTITY fill_color .*>', entity, data)

		entity = '<!ENTITY stroke_color "%s">' % dict.get('stroke_color', '')
		data = re.sub('<!ENTITY stroke_color .*>', entity, data)
		
		entity = '<!ENTITY opacity "%s">' % dict.get('opacity', '')
		data = re.sub('<!ENTITY opacity .*>', entity, data)
				
		data = re.sub('size_card1', str(self.size), data)
		data = re.sub('size_card2', str(self.size-6), data)
		data = re.sub('size_card3', str(self.size-17), data)
		pixbuf = rsvg.Handle(data=data).get_pixbuf()
		self.cache[set] = pixbuf
		return pixbuf
	
	def set_border(self, stroke_color, fill_color):
		self.props['front'].update({'fill_color':fill_color, 'stroke_color':stroke_color})
		self.queue_draw()
		while gtk.events_pending():
			gtk.main_iteration()		
	
	def set_pixbuf(self, pixbuf):
		if pixbuf == None:
			self.jpeg = None
			self.show_jpeg = False
		else:
			if self.jpeg != None:
				del self.jpeg
				
			self.jpeg = pixbuf
			del pixbuf
			self.show_jpeg = True
		
		self.queue_draw()
		while gtk.events_pending():
			gtk.main_iteration()
	
	def get_pixbuf(self):
		return self.jpeg
		
	def set_highlight(self, status, mouse = False):
		if self.flipped:
			if mouse:
				return
			if status:
				self.current_face = 'front_h'
			else:
				self.current_face = 'front'
		else:  
			if status:
				self.current_face = 'back_h'
			else:
				self.current_face = 'back'
		self.queue_draw()				 
			
	def flip(self):
		if not self.flipped:
			if not self.flipped_once:
				if self.jpeg <> None:
					pixbuf_t = gtk.gdk.pixbuf_new_from_file(self.jpeg)
					if pixbuf_t.get_width() != self.size-22 or pixbuf_t.get_height() != self.size-22:
						self.jpeg = pixbuf_t.scale_simple(self.size-22, self.size-22, gtk.gdk.INTERP_BILINEAR)
						del pixbuf_t
					else:
						self.jpeg = pixbuf_t
				text = self.props.get('front_text', {}).get('card_text', '')		
				if text != None and len(text) > 0:
					self.front_layout = self.get_text_layout(self.props['front_text']['card_text'], self.size-12)
					self.front_layout_position = (self.size -(self.front_layout.get_size()[1]/1000))/2
				self.flipped_once = True
			
			if self.jpeg <> None:
				self.show_jpeg = True
			text = self.props.get('front_text', {}).get('card_text', '')		
			if text != None and len(text) > 0:
				self.current_layout = self.front_layout
				self.current_layout_position = self.front_layout_position
				self.current_text_color = self.props['front_text']['text_color']
				self.show_text = True
			else:
				self.show_text = False

			self.current_face = 'front'

			self.flipped  = True
			self.queue_draw()
			
			while gtk.events_pending():
				gtk.main_iteration()	
			gc.collect()		
	
	def flop(self):
		self.current_face = 'back'
		if len(self.props['back_text'].get('card_text', '')) > 0:
			self.current_layout = self.back_layout
			self.current_layout_position = self.back_layout_position
			self.current_text_color = self.props['back_text']['text_color']
			self.show_text = True
		else:
			self.show_text = False
		self.flipped = False
		self.show_jpeg = False
		self.queue_draw()
		
	def is_flipped(self):
		return self.flipped
		
	def get_id(self):
		return self.id
	
	def reset(self):
		if self.flipped:
			fill_color = self.default_props.get('front_border').get('fill_color')
			stroke_color = self.default_propsfront_text.get('front_border').get('stroke_color')
			self.set_border(fill_color, stroke_color)
			self.flop()
			
	def get_text_layout(self, text, size):
		if self.size == 119:
			font_sizes = [30, 24, 16, 13, 10, 8, 8, 8]
		elif self.size == 145: 
			font_sizes = [45, 28, 20, 16, 13, 11, 9, 8] 
		else:
			font_sizes = [50, 40, 26, 20, 17, 13, 11, 8] 
		# Set font size considering string length
		if len(text) <= 8:
			font_size = font_sizes[len(text)-1]
		else: 
			font_size = 8

		# Set Pango context and Pango layout
		context = self.create_pango_context()
		layout = self.create_pango_layout(text)
		desc = pango.FontDescription('Deja Vu Sans bold '+str(font_size))
		layout.set_font_description(desc)	
		layout.set_alignment(pango.ALIGN_CENTER)
		layout.set_width(size*1000)
		return layout

	def set_background(self, color):
		self.bg_color = color
		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.bg_color))
	
	def change_text(self, newtext):
		self.props['front_text']['card_text'] = newtext
		self.front_layout = self.get_text_layout(self.props['front_text'].get('card_text', ''), self.size-11)	
		if self.align == '2': # top
			self.front_layout_position = 6
		elif self.align == '3': # bottom
			self.front_layout_position = self.size -(self.front_layout.get_size()[1]/1000)
		else: # center and none
			self.front_layout_position = (self.size -(self.front_layout.get_size()[1]/1000))/2
			
		self.current_layout = self.front_layout
		self.current_layout_position = self.front_layout_position
		self.current_text_color = self.props['front_text']['text_color']
		if len(newtext) > 0:
			self.show_text = True
		self.queue_draw()		
	def get_text(self):
		return self.props['front_text'].get('card_text', '')
