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
import os
import shutil
import tempfile
from gettext import gettext as _
import svgcard
import logging
import gobject
from xml.dom.minidom import parse
from sugar.graphics.objectchooser import ObjectChooser

_logger = logging.getLogger('memorize-activity')

class CreateCardPanel(gtk.EventBox):
	
	__gsignals__ = {
		'add-pair': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT]), 
		'update-pair': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT]), 
	}
	
	def __init__(self):
		gtk.EventBox.__init__(self)
		self.set_size_request(650, 320)
		
		self.equal_pairs = False
		
		# Set the add new pair buttom
		add_icon = os.path.join(os.path.dirname(__file__), "images/pair-add.svg")
		add_image = gtk.Image()
		add_image.set_from_file(add_icon)
		self._addbutton = gtk.Button(' ' + _('Add as new pair'))
		self._addbutton.set_image(add_image)
		self._addbutton.connect('button-press-event', self.emit_add_pair)
		
		# Set update selected pair buttom
		update_icon = os.path.join(os.path.dirname(__file__), "images/pair-update.svg")
		update_image = gtk.Image()
		update_image.set_from_file(update_icon)
		self._updatebutton = gtk.Button(' ' + _('Update selected pair'))
		self._updatebutton.set_image(update_image)
		self._updatebutton.connect('button-press-event', self.emit_update_pair)
		
		# Set card editors
		self.cardeditor1 = CardEditor()
		self.cardeditor2 = CardEditor()
		self.clean(None)
		self.cardeditor1.connect('has-text', self.receive_text_signals)
		self.cardeditor2.connect('has-text', self.receive_text_signals)
		self.cardeditor1.connect('has-picture', self.receive_picture_signals)
		self.cardeditor2.connect('has-picture', self.receive_picture_signals)
		
		# Create table and add components to the table
		self.table = gtk.Table()
		self.table.set_homogeneous(False)
		self.table.set_col_spacings(10)
		self.table.set_row_spacings(10)
		self.table.set_border_width(10)
		self.table.attach(self.cardeditor1, 0, 2, 0, 1, gtk.SHRINK|gtk.FILL, gtk.SHRINK, 10, 30)
		self.table.attach(self.cardeditor2, 2, 4, 0, 1, gtk.SHRINK|gtk.FILL, gtk.SHRINK, 10, 30)
		self.table.attach(self._addbutton, 1, 2, 1, 2, gtk.SHRINK|gtk.FILL, gtk.SHRINK)
		self.table.attach(self._updatebutton, 2, 3, 1, 2, gtk.SHRINK|gtk.FILL, gtk.SHRINK)
		self.add(self.table)
		self.show_all()
		
	def emit_add_pair(self, widget, event):
		if self.equal_pairs:
			self.emit('add-pair', self.cardeditor1.get_text(), self.cardeditor1.get_text(), self.cardeditor1.get_pixbuf(), self.cardeditor1.get_pixbuf(), self.cardeditor1.get_snd(), self.cardeditor1.get_snd())
		else:
			self.emit('add-pair', self.cardeditor1.get_text(), self.cardeditor2.get_text(), self.cardeditor1.get_pixbuf(), self.cardeditor2.get_pixbuf(), self.cardeditor1.get_snd(), self.cardeditor2.get_snd())
		self.clean(None)
		

	def emit_update_pair(self, widget, event):
		if self.equal_pairs:
			self.emit('update-pair', self.cardeditor1.get_text(), self.cardeditor1.get_text(), self.cardeditor1.get_pixbuf(), self.cardeditor1.get_pixbuf(), self.cardeditor1.get_snd(), self.cardeditor1.get_snd())
		else:
			self.emit('update-pair', self.cardeditor1.get_text(), self.cardeditor2.get_text(), self.cardeditor1.get_pixbuf(), self.cardeditor2.get_pixbuf(), self.cardeditor1.get_snd(), self.cardeditor2.get_snd())
		self.clean(None)
					
	def load_pair(self, widget, newtext1, newtext2, aimg, bimg, asnd, bsnd):
		self.cardeditor1.set_text(newtext1)
		self.cardeditor2.set_text(newtext2)
		self.cardeditor1.set_pixbuf(aimg)
		self.cardeditor2.set_pixbuf(bimg)
		self.cardeditor1.set_snd(asnd)
		self.cardeditor2.set_snd(bsnd)
		self._addbutton.set_sensitive(True)
		self._updatebutton.set_sensitive(True)

	def change_equal_pairs(self, widget, state):
		self.equal_pairs = state
		self.clean(None)
		if self.equal_pairs:
			self.table.remove(self.cardeditor1)
			self.table.remove(self.cardeditor2)
			self.table.attach(self.cardeditor1, 0, 4, 0, 1, gtk.SHRINK|gtk.FILL, gtk.SHRINK, 200, 30)
		else:
			self.table.remove(self.cardeditor1)
			self.table.attach(self.cardeditor1, 0, 2, 0, 1, gtk.SHRINK|gtk.FILL, gtk.SHRINK, 10, 30)
			self.table.attach(self.cardeditor2, 2, 4, 0, 1, gtk.SHRINK|gtk.FILL, gtk.SHRINK, 10, 30)
	
	def clean(self, widget):
		self.cardeditor1.clean()
		self.cardeditor2.clean()
		self._addbutton.set_sensitive(False)
		self._updatebutton.set_sensitive(False)
		self._card1_has_text = False
		self._card2_has_text = False
		self._card1_has_picture = False
		self._card2_has_picture = False
		
	def receive_text_signals(self, widget, has_text):
		if widget == self.cardeditor1:
			self._card1_has_text = has_text
		if widget == self.cardeditor2:
			self._card2_has_text = has_text
		self._update_buttom_status()
		
	def receive_picture_signals(self, widget, has_picture):
		if widget == self.cardeditor1:
			self._card1_has_picture = has_picture
		if widget == self.cardeditor2:
			self._card2_has_picture = has_picture
		self._update_buttom_status()
		
	def _update_buttom_status(self):
		if not self.equal_pairs:
			if (self._card1_has_text or self._card1_has_picture) and (self._card2_has_text or self._card2_has_picture):
				self._addbutton.set_sensitive(True)
				self._updatebutton.set_sensitive(True)
			else:
				self._addbutton.set_sensitive(False)
				self._updatebutton.set_sensitive(False)
		else:
			if self._card1_has_text or self._card1_has_picture:
				self._addbutton.set_sensitive(True)
				self._updatebutton.set_sensitive(True)
			else:
				self._addbutton.set_sensitive(False)
				self._updatebutton.set_sensitive(False)
				
class CardEditor(gtk.EventBox):
	
	__gsignals__ = {
		'has-text': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT]), 
		'has-picture': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT]), 
	}
	
	def __init__(self):
		gtk.EventBox.__init__(self)
		self.set_size_request(310, 320)

		self.temp_folder = tempfile.mkdtemp()
		
		table = gtk.Table()
		self.previewlabel = gtk.Label(_('Preview:'))
		self.previewlabel.set_alignment(1, 0.5)
		self.textlabel = gtk.Label(_('Text:'))
		self.textlabel.set_alignment(1, 0.5)
		
		picture_icon = os.path.join(os.path.dirname(__file__), 'images/import_picture.svg')
		picture_image = gtk.Image()
		picture_image.set_from_file(picture_icon)
		self.browsepicture = gtk.Button()
		self.browsepicture.set_image(picture_image)
		self.browsepicture.connect('button-press-event', self._import_image)
		
		sound_icon = os.path.join(os.path.dirname(__file__), 'images/import_sound.svg')
		sound_image = gtk.Image()
		sound_image.set_from_file(sound_icon)
		self.browsesound = gtk.Button()
		self.browsesound.set_image(sound_image)
		self.browsesound.connect('button-press-event', self._import_audio)
		self.snd = None
		self.textentry = gtk.Entry()
		self.textentry.connect('changed', self.update_text)
				
		table.set_homogeneous(False)
		table.set_col_spacings(10)
		table.set_row_spacings(10)
		table.set_border_width(10)
		self.card = svgcard.SvgCard(-1, {'front_text':{'card_text':'', 'text_color':'#ffffff'}, 'front_border':{'fill_color':'#4c4d4f', 'stroke_color':'#ffffff', 'opacity':'1'}}, None, 184, 1, '#c0c0c0')
		self.card.flip()
		
		table.attach(self.previewlabel, 0, 1, 1, 2, gtk.EXPAND, gtk.EXPAND)
		table.attach(self.card, 1, 3, 1, 2, gtk.EXPAND, gtk.EXPAND, 10)
		#Text label and entry
		table.attach(self.textlabel, 0, 1, 2, 3, gtk.EXPAND|gtk.FILL, gtk.EXPAND)
		table.attach(self.textentry, 1, 3, 2, 3, gtk.EXPAND|gtk.FILL, gtk.EXPAND)
		#Picture label and entry
		table.attach(self.browsepicture, 1, 2, 3, 4, gtk.EXPAND|gtk.FILL, gtk.EXPAND)
		#Sound label and entry
		table.attach(self.browsesound, 2, 3, 3, 4, gtk.EXPAND|gtk.FILL, gtk.EXPAND)
		
		self.add(table)
		
	def update_text(self, entry):
		self.card.change_text(entry.get_text())
		if len(entry.get_text()) == 0:
			self.emit('has-text', False)
		else:
			self.emit('has-text', True)
		
	def get_text(self):
		return self.textentry.get_text()

	def set_text(self, newtext):
		if newtext == None:
			newtext = ''
		self.textentry.set_text(newtext)
		
	def get_pixbuf(self):
		return self.card.get_pixbuf()
	
	def set_pixbuf(self, pixbuf):
		self.card.set_pixbuf(pixbuf)
		
	def _import_image(self, widget, event):
		chooser = ObjectChooser(_('Choose image'), None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
		try:
			result = chooser.run()
			if result == gtk.RESPONSE_ACCEPT:
				_logger.debug('ObjectChooser: %r' % chooser.get_selected_object())
				jobject = chooser.get_selected_object()
				if jobject and jobject.file_path:
					self._load_image(jobject.file_path)
		finally:
			chooser.destroy()
			del chooser
			
	def _load_image(self, index):
		pixbuf_t = gtk.gdk.pixbuf_new_from_file(index)
		self.card.set_pixbuf(self.to_card_pixbuf(pixbuf_t))	
		_logger.error('Picture Loaded: '+index)
		self.emit('has-picture', True)
		del pixbuf_t
		
	def _import_audio(self, widget, event):
		chooser = ObjectChooser(_('Choose audio'), None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
		jobject = ''
		try:
			result = chooser.run()
			if result == gtk.RESPONSE_ACCEPT:
				_logger.debug('ObjectChooser: %r' % chooser.get_selected_object())
				jobject = chooser.get_selected_object()
				if not jobject or  not jobject.file_path:
					return
		finally:
			chooser.destroy()
			del chooser
			
		if jobject and jobject.file_path:	
			self._load_audio(jobject.file_path)
			
	def _load_audio(self, index):
		dst = os.path.join(self.temp_folder, os.path.basename(index))
		shutil.copy(index, dst)
		self.set_snd(dst)
		_logger.error('Audio Loaded: '+dst)
	
	def set_snd(self, snd):
		self.snd = snd
	
	def get_snd(self):
		return self.snd	

	def clean(self):
		self.textentry.set_text('')
		self.card.set_pixbuf(None)
		self.emit('has-text', False)
		self.emit('has-picture', False)	
	
	def to_card_pixbuf(self, pixbuf):
		if pixbuf.get_width() == pixbuf.get_height():
			new = pixbuf_t.scale_simple(162, 162, gtk.gdk.INTERP_BILINEAR)
		elif pixbuf.get_width() > pixbuf.get_height():
			new = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 162, 162)
			aspect = float(pixbuf.get_width()) / float(pixbuf.get_height())
			pixbuf_t = pixbuf.scale_simple(int(float(162)*aspect) , 162, gtk.gdk.INTERP_BILINEAR)
			diff = pixbuf_t.get_width() - pixbuf_t.get_height()
			pixbuf_t.scale(new, 0, 0, 162, 162, -(diff/2), 0, 1, 1, gtk.gdk.INTERP_BILINEAR)
			del pixbuf_t
		elif pixbuf.get_width() < pixbuf.get_height():	
			new = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 162, 162)
			aspect = float(pixbuf.get_height()) / float(pixbuf.get_width())
			pixbuf_t = pixbuf.scale_simple(162 , int(float(162)*aspect), gtk.gdk.INTERP_BILINEAR)
			diff = pixbuf_t.get_height() - pixbuf_t.get_width()
			pixbuf_t.scale(new, 0, 0, 162, 162, 0, -(diff/2), 1, 1, gtk.gdk.INTERP_BILINEAR)
			del pixbuf_t
		return new	