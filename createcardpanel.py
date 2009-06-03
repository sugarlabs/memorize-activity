#
#    Copyright (C) 2006, 2007, 2008 One Laptop Per Child
#    Copyright (C) 2009 Simon Schampijer
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
from os import environ
from os.path import join, dirname, basename

import shutil
import tempfile
from gettext import gettext as _
import svgcard
import logging
from gobject import SIGNAL_RUN_FIRST, TYPE_PYOBJECT
from xml.dom.minidom import parse
from sugar.graphics.objectchooser import ObjectChooser
from sugar import mime
from sugar.graphics import style

import theme

_logger = logging.getLogger('memorize-activity')

class CreateCardPanel(gtk.EventBox):
    
    __gsignals__ = {
        'add-pair': (SIGNAL_RUN_FIRST, None, 6 * [TYPE_PYOBJECT]), 
        'update-pair': (SIGNAL_RUN_FIRST, None, 6 * [TYPE_PYOBJECT]), 
    }
    
    def __init__(self):
        gtk.EventBox.__init__(self)
        
        self.equal_pairs = False
        self._updatebutton_sensitive = False
        
        # Set the add new pair buttom
        add_icon = join(dirname(__file__), 'images', 'pair-add.svg')
        add_image = gtk.Image()
        add_image.set_from_file(add_icon)
        self._addbutton = gtk.Button(' ' + _('Add as new pair'))
        self._addbutton.set_image(add_image)
        self._addbutton.connect('pressed', self.emit_add_pair)
        self._addbutton.set_size_request(
                theme.PAIR_SIZE + theme.PAD*4, -1)
        
        # Set update selected pair buttom
        update_icon = join(dirname(__file__), 'images', 'pair-update.svg')
        update_image = gtk.Image()
        update_image.set_from_file(update_icon)
        self._updatebutton = gtk.Button(' ' + _('Update selected pair'))
        self._updatebutton.set_image(update_image)
        self._updatebutton.connect('pressed', self.emit_update_pair)
        self._updatebutton.set_size_request(
                theme.PAIR_SIZE + theme.PAD*4, -1)
        
        # Set card editors
        self.cardeditor1 = CardEditor()
        self.cardeditor2 = CardEditor()
        self.clean(None)
        self.cardeditor1.connect('has-text', self.receive_text_signals)
        self.cardeditor2.connect('has-text', self.receive_text_signals)
        self.cardeditor1.connect('has-picture', self.receive_picture_signals)
        self.cardeditor2.connect('has-picture', self.receive_picture_signals)
        self.cardeditor1.connect('has-sound', self.receive_sound_signals)
        self.cardeditor2.connect('has-sound', self.receive_sound_signals)
        
        # Create table and add components to the table
        self.table = gtk.Table()
        self.table.set_homogeneous(False)
        self.table.set_col_spacings(theme.PAD)
        self.table.set_row_spacings(theme.PAD)
        self.table.set_border_width(theme.PAD)
        self.table.attach(self.cardeditor1, 0, 1, 0, 1, yoptions=gtk.SHRINK)
        self.table.attach(self.cardeditor2, 1, 2, 0, 1, yoptions=gtk.SHRINK)
        self.table.attach(self._addbutton, 0, 1, 1, 2, yoptions=gtk.SHRINK)
        self.table.attach(self._updatebutton, 1, 2, 1, 2, yoptions=gtk.SHRINK)
        self.add(self.table)
        self.show_all()
        
    def emit_add_pair(self, widget):
        self._addbutton.set_sensitive(False)
        if self.equal_pairs:
            self.emit('add-pair', self.cardeditor1.get_text(), 
                      self.cardeditor1.get_text(), 
                      self.cardeditor1.get_pixbuf(), 
                      self.cardeditor1.get_pixbuf(), 
                      self.cardeditor1.get_snd(), self.cardeditor1.get_snd())
        else:
            self.emit('add-pair', self.cardeditor1.get_text(), 
                      self.cardeditor2.get_text(), 
                      self.cardeditor1.get_pixbuf(), 
                      self.cardeditor2.get_pixbuf(), 
                      self.cardeditor1.get_snd(), self.cardeditor2.get_snd())
        self.clean(None)
        

    def emit_update_pair(self, widget):
        self._addbutton.set_sensitive(False)
        if self.equal_pairs:
            self.emit('update-pair', self.cardeditor1.get_text(), 
                      self.cardeditor1.get_text(), 
                      self.cardeditor1.get_pixbuf(), 
                      self.cardeditor1.get_pixbuf(), 
                      self.cardeditor1.get_snd(), self.cardeditor1.get_snd())
        else:
            self.emit('update-pair', self.cardeditor1.get_text(), 
                      self.cardeditor2.get_text(), 
                      self.cardeditor1.get_pixbuf(), 
                      self.cardeditor2.get_pixbuf(), 
                      self.cardeditor1.get_snd(), self.cardeditor2.get_snd())
        self.clean(None)
                    
    def pair_selected(self, widget, selected, newtext1, newtext2, aimg, bimg,
            asnd, bsnd):
        if selected:
            self.cardeditor1.set_text(newtext1)
            self.cardeditor2.set_text(newtext2)
            self.cardeditor1.set_pixbuf(aimg)
            self.cardeditor2.set_pixbuf(bimg)
            self.cardeditor1.set_snd(asnd)
            self.cardeditor2.set_snd(bsnd)
            self._addbutton.set_sensitive(True)
        self._updatebutton.set_sensitive(selected)
        self._updatebutton_sensitive = selected

    def change_equal_pairs(self, widget, state):
        self.equal_pairs = state
        self.clean(None)
        if self.equal_pairs:
            self.table.remove(self.cardeditor1)
            self.table.remove(self.cardeditor2)
            self.table.attach(self.cardeditor1, 0, 2, 0, 1,
                    gtk.SHRINK, gtk.SHRINK)
        else:
            self.table.remove(self.cardeditor1)
            self.table.attach(self.cardeditor1, 0, 1, 0, 1, yoptions=gtk.SHRINK)
            self.table.attach(self.cardeditor2, 1, 2, 0, 1, yoptions=gtk.SHRINK)
    
    def clean(self, widget):
        self.cardeditor1.clean()
        self.cardeditor2.clean()
        self._addbutton.set_sensitive(False)
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
        
    def receive_sound_signals(self, widget, has_sound):
        if widget == self.cardeditor1:
            self._card1_has_sound = has_sound
        if widget == self.cardeditor2:
            self._card2_has_sound = has_sound
        self._update_buttom_status()
        
    def _update_buttom_status(self):
        if not self.equal_pairs:
            if (self._card1_has_text or self._card1_has_picture or self._card1_has_sound) and (self._card2_has_text or self._card2_has_picture or self._card2_has_sound):
                self._addbutton.set_sensitive(True)
                self._updatebutton.set_sensitive(self._updatebutton_sensitive)
            else:
                self._addbutton.set_sensitive(False)
                self._updatebutton.set_sensitive(False)
        else:
            if self._card1_has_text or self._card1_has_picture or self._card1_has_sound:
                self._addbutton.set_sensitive(True)
                self._updatebutton.set_sensitive(self._updatebutton_sensitive)
            else:
                self._addbutton.set_sensitive(False)
                self._updatebutton.set_sensitive(False)
                
class CardEditor(gtk.EventBox):
    
    __gsignals__ = {
        'has-text': (SIGNAL_RUN_FIRST, None, [TYPE_PYOBJECT]), 
        'has-picture': (SIGNAL_RUN_FIRST, None, [TYPE_PYOBJECT]), 
        'has-sound': (SIGNAL_RUN_FIRST, None, [TYPE_PYOBJECT]), 
    }
    
    def __init__(self):
        gtk.EventBox.__init__(self)

        tmp_root = join(environ['SUGAR_ACTIVITY_ROOT'], 'instance')
        self.temp_folder = tempfile.mkdtemp(dir=tmp_root)
        
        table = gtk.Table()
        self.previewlabel = gtk.Label(_('Preview:'))
        self.previewlabel.set_alignment(0, 1)
        self.textlabel = gtk.Label(_('Text:'))
        self.textlabel.set_alignment(0, 1)
        
        picture_icon = join(dirname(__file__), 'images', 'import_picture.svg')
        picture_image = gtk.Image()
        picture_image.set_from_file(picture_icon)
        self.browsepicture = gtk.Button()
        self.browsepicture.set_image(picture_image)
        self.browsepicture.connect('button-press-event', self._import_image)
        
        sound_icon = join(dirname(__file__), 'images', 'import_sound.svg')
        sound_image = gtk.Image()
        sound_image.set_from_file(sound_icon)
        self.browsesound = gtk.Button()
        self.browsesound.set_image(sound_image)
        self.browsesound.connect('button-press-event', self._import_audio)
        self.snd = None
        self.textentry = gtk.Entry()
        self.textentry.connect('changed', self.update_text)
                
        table.set_homogeneous(False)
        table.set_col_spacings(theme.PAD)
        table.set_row_spacings(theme.PAD)
        table.set_border_width(theme.PAD)
        self.card = svgcard.SvgCard(-1,
                { 'front_text'  : { 'card_text'     : '',
                                    'text_color'    : '#ffffff' },
                  'front_border': { 'fill_color'    : '#4c4d4f',
                                    'stroke_color'  : '#ffffff',
                                    'opacity'       : '1' } },
                None, theme.PAIR_SIZE, 1, '#c0c0c0')
        self.card.flip()
        
        table.attach(self.previewlabel, 0, 2, 0, 1, yoptions=gtk.SHRINK)
        table.attach(self.card, 0, 2, 1, 2, gtk.SHRINK, gtk.SHRINK,
                theme.PAD)
        #Text label and entry
        table.attach(self.textlabel, 0, 1, 2, 3, yoptions=gtk.SHRINK)
        table.attach(self.textentry, 0, 2, 3, 4, yoptions=gtk.SHRINK)
        self.textentry.set_size_request(0, -1)
        #Picture label and entry
        table.attach(self.browsepicture, 0, 1, 4, 5, yoptions=gtk.SHRINK)
        #Sound label and entry
        table.attach(self.browsesound, 1, 2, 4, 5, yoptions=gtk.SHRINK)
        
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
        if hasattr(mime, 'GENERIC_TYPE_IMAGE'):
            filter = { 'what_filter': mime.GENERIC_TYPE_IMAGE }
        else:
            filter = { }

        chooser = ObjectChooser(_('Choose image'), None,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                **filter)
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
        pixbuf_t = gtk.gdk.pixbuf_new_from_file_at_size(
            index, theme.PAIR_SIZE - theme.PAD*2, theme.PAIR_SIZE - theme.PAD*2)
        if pixbuf_t.get_width() > pixbuf_t.get_height():
            size = pixbuf_t.get_width()
        else:
            size = pixbuf_t.get_height()
        pixbuf_z = gtk.gdk.pixbuf_new_from_file_at_size(
            'images/white.png', size, size)    
        pixbuf_t.composite(pixbuf_z, 0, 0, pixbuf_t.get_width(), 
                           pixbuf_t.get_height(), 0, 0, 1, 1, 
                           gtk.gdk.INTERP_BILINEAR, 255)
        self.card.set_pixbuf(pixbuf_z)
        _logger.error('Picture Loaded: '+index)
        self.emit('has-picture', True)
        del pixbuf_t
        del pixbuf_z
        
    def _import_audio(self, widget, event):
        if hasattr(mime, 'GENERIC_TYPE_AUDIO'):
            filter = { 'what_filter': mime.GENERIC_TYPE_AUDIO }
        else:
            filter = { }

        chooser = ObjectChooser(_('Choose audio'), None,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                **filter)
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
        dst = join(self.temp_folder, basename(index))
        shutil.copy(index, dst)
        self.set_snd(dst)
        icon_theme = gtk.icon_theme_get_default()
        pixbuf_t = icon_theme.load_icon("audio-x-generic",
                                        style.XLARGE_ICON_SIZE, 0)
        self.card.set_pixbuf(pixbuf_t)    
        self.emit('has-sound', True)
        _logger.debug('Audio Loaded: '+dst)
    
    def set_snd(self, snd):
        self.snd = snd
    
    def get_snd(self):
        return self.snd    

    def clean(self):
        self.textentry.set_text('')
        self.card.set_pixbuf(None)
        self.snd = None
        self.emit('has-text', False)
        self.emit('has-picture', False)
        self.emit('has-sound', False)
