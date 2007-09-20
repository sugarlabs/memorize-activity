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
import logging
import gobject

_logger = logging.getLogger('memorize-activity')

class CreateCardPanel(gtk.EventBox):
	
	__gsignals__ = {
		'add-pair': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT]), 
		'update-pair': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT,gobject.TYPE_PYOBJECT]), 
	}
	
	def __init__(self):
		gtk.EventBox.__init__(self)
		
		table = gtk.Table()
		table.set_col_spacings(10)
		table.set_row_spacings(10)
		table.set_border_width(200)
		
		addbutton = gtk.Button('Add as new pair')
		addbutton.connect('button-press-event',self.emit_add_pair)
		
		updatebutton = gtk.Button('Update selected pair')
		updatebutton.connect('button-press-event',self.emit_update_pair)
		
		self.cardeditor = CardEditor()
		table.attach(self.cardeditor, 0, 2, 0, 1)
		table.attach(addbutton, 0, 1, 1, 2)
		table.attach(updatebutton, 1, 2, 1, 2)
		
		self.add(table)
		self.show_all()
		
	def emit_add_pair(self, widget, event):
		self.emit('add-pair',self.cardeditor.get_text(),self.cardeditor.get_text())

	def emit_update_pair(self, widget, event):
		self.emit('update-pair',self.cardeditor.get_text(),self.cardeditor.get_text())
		
	def load_pair(self, widget, newtext):
		self.cardeditor.set_text(newtext)

class CardEditor(gtk.EventBox):
	
	def __init__(self):
		gtk.EventBox.__init__(self)
		self.set_size_request(400, 400)

		table = gtk.Table()
		self.previewlabel = gtk.Label('Preview:')
		self.previewlabel.set_alignment(1, 0.5)
		self.textlabel = gtk.Label('Text:')
		self.textlabel.set_alignment(1, 0.5)
		self.picturelabel = gtk.Label('Picture:')
		self.picturelabel.set_alignment(1, 0.5)
		self.soundlabel = gtk.Label('Sound:')
		self.soundlabel.set_alignment(1, 0.5)
		
		self.browsepicture = gtk.Button('Browse')
		self.capturepicture = gtk.Button('Capture')
		self.browsesound = gtk.Button('Browse')
		self.recordsound = gtk.Button('Record')
		self.textentry = gtk.Entry()
		self.textentry.connect('changed', self.update_text)
				
		table.set_col_spacings(10)
		table.set_row_spacings(10)
		table.set_border_width(20)
		self.card = svgcard.SvgCard(-1, {'front_text':{'card_text':'', 'text_color':'#ffffff'}, 'front_border':{'fill_color':'#4c4d4f', 'stroke_color':'#ffffff', 'opacity':'1'}}, None, 184, 1, '#c0c0c0')
		self.card.flip()
		
		table.attach(self.previewlabel, 0, 1, 1, 2)
		table.attach(self.card, 1, 3, 1, 2)
		#Text label and entry
		table.attach(self.textlabel, 0, 1, 2, 3)
		table.attach(self.textentry, 1, 3, 2, 3)
		#Picture label and entry
		table.attach(self.picturelabel, 0, 1, 3, 4)
		table.attach(self.browsepicture, 1, 2, 3, 4)
		table.attach(self.capturepicture, 2, 3, 3, 4)
		#Sound label and entry
		table.attach(self.soundlabel, 0, 1, 4, 5)
		table.attach(self.browsesound, 1, 2, 4, 5)
		table.attach(self.recordsound, 2, 3, 4, 5)
		
		self.add(table)
		
	def update_text(self, entry):
		self.card.change_text(entry.get_text())
		
	def get_text(self):
		return self.textentry.get_text()

	def set_text(self, newtext):
		self.textentry.set_text(newtext)
