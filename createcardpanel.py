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

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GdkPixbuf

from os.path import join, basename

import shutil
from gettext import gettext as _
import svgcard
import logging

from sugar3.graphics import style
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.icon import Icon
from sugar3.graphics.palette import Palette
from sugar3.graphics.toggletoolbutton import ToggleToolButton
from sugar3.graphics.toolcombobox import ToolComboBox
from fontcombobox import FontComboBox
from port import chooser

import theme
import speak.espeak
import speak.widgets
import speak.face
from port.roundbox import RoundBox
import model

_logger = logging.getLogger('memorize-activity')


class CreateCardPanel(Gtk.EventBox):
    __gsignals__ = {
        'add-pair': (GObject.SignalFlags.RUN_FIRST, None, 10 * [GObject.TYPE_PYOBJECT]),
        'update-pair': (GObject.SignalFlags.RUN_FIRST, None, 8 * [GObject.TYPE_PYOBJECT]),
        'change-font': (GObject.SignalFlags.RUN_FIRST, None, 2 * [GObject.TYPE_PYOBJECT]),
    }

    def __init__(self):
        def make_label(icon_name, label):
            label_box = Gtk.HBox()
            icon = Icon(
                    icon_name=icon_name,
                    icon_size=Gtk.IconSize.LARGE_TOOLBAR)
            label_box.pack_start(icon, False)
            label = Gtk.Label(label=label)
            label.modify_fg(Gtk.StateType.NORMAL,
                    style.COLOR_TOOLBAR_GREY.get_gdk_color())
            label_box.pack_start(label, True, True, 0)
            label_box.show_all()
            return label_box

        Gtk.EventBox.__init__(self)

        self.equal_pairs = False
        self._updatebutton_sensitive = False
        self._card1_has_sound = False
        self._card2_has_sound = False

        # save buttons

        buttons_bar = Gtk.HBox()
        buttons_bar.props.border_width = 10

        self._addbutton = ToolButton(
                tooltip=_('Add as new pair'),
                sensitive=False)
        self._addbutton.set_icon_widget(
                make_label('pair-add', ' ' + _('Add')))
        self._addbutton.connect('clicked', self.emit_add_pair)
        buttons_bar.pack_start(self._addbutton, False)

        self._updatebutton = ToolButton(
                tooltip=_('Update selected pair'),
                sensitive=False)
        self._updatebutton.set_icon_widget(
                make_label('pair-update', ' ' + _('Update')))
        self._updatebutton.connect('clicked', self.emit_update_pair)
        buttons_bar.pack_start(self._updatebutton, False)

        # Set card editors

        self.cardeditor1 = CardEditor(1)
        self.cardeditor2 = CardEditor(2)
        self.clean(None)
        self.cardeditor1.connect('has-text', self.receive_text_signals)
        self.cardeditor2.connect('has-text', self.receive_text_signals)
        self.cardeditor1.connect('has-picture', self.receive_picture_signals)
        self.cardeditor2.connect('has-picture', self.receive_picture_signals)
        self.cardeditor1.connect('has-sound', self.receive_sound_signals)
        self.cardeditor2.connect('has-sound', self.receive_sound_signals)
        self.cardeditor1.connect('change-font', self.receive_font_signals)
        self.cardeditor2.connect('change-font', self.receive_font_signals)

        # edit panel

        self.card_box = Gtk.HBox()
        self.card_box.pack_start(self.cardeditor1, True, True, 0)
        self.card_box.pack_start(self.cardeditor2, True, True, 0)

        box = Gtk.VBox()
        box.pack_start(self.card_box, False)
        box.pack_start(buttons_bar, False)
        self.add(box)

        self.show_all()

    def update_font_combos(self, widget, data, grid):
        logging.error('update font %s', data)
        if 'font_name1' in  data:
            self.cardeditor1.set_font_name(data['font_name1'])
            self.cardeditor1.card.change_font(data['font_name1'])
        if 'font_name2' in  data:
            self.cardeditor2.set_font_name(data['font_name2'])
            self.cardeditor2.card.change_font(data['font_name2'])

    def emit_add_pair(self, widget):
        self._addbutton.set_sensitive(False)
        if self.equal_pairs:
            self.emit('add-pair', self.cardeditor1.get_text(),
                      self.cardeditor1.get_text(),
                      self.cardeditor1.get_pixbuf(),
                      self.cardeditor1.get_pixbuf(),
                      self.cardeditor1.get_snd(),
                      self.cardeditor1.get_snd(),
                      self.cardeditor1.get_speak(),
                      self.cardeditor1.get_speak(),
                      self.cardeditor1.get_font_name(),
                      self.cardeditor1.get_font_name())
        else:
            self.emit('add-pair', self.cardeditor1.get_text(),
                      self.cardeditor2.get_text(),
                      self.cardeditor1.get_pixbuf(),
                      self.cardeditor2.get_pixbuf(),
                      self.cardeditor1.get_snd(),
                      self.cardeditor2.get_snd(),
                      self.cardeditor1.get_speak(),
                      self.cardeditor2.get_speak(),
                      self.cardeditor1.get_font_name(),
                      self.cardeditor2.get_font_name())
        self.clean(None)

    def emit_update_pair(self, widget):
        self._addbutton.set_sensitive(False)
        if self.equal_pairs:
            self.emit('update-pair', self.cardeditor1.get_text(),
                      self.cardeditor1.get_text(),
                      self.cardeditor1.get_pixbuf(),
                      self.cardeditor1.get_pixbuf(),
                      self.cardeditor1.get_snd(),
                      self.cardeditor1.get_snd(),
                      self.cardeditor1.get_speak(),
                      self.cardeditor1.get_speak())
        else:
            self.emit('update-pair', self.cardeditor1.get_text(),
                      self.cardeditor2.get_text(),
                      self.cardeditor1.get_pixbuf(),
                      self.cardeditor2.get_pixbuf(),
                      self.cardeditor1.get_snd(),
                      self.cardeditor2.get_snd(),
                      self.cardeditor1.get_speak(),
                      self.cardeditor2.get_speak())
        self.clean(None)

    def pair_selected(self, widget, selected, newtext1, newtext2, aimg, bimg,
            asnd, bsnd, aspeak, bspeak):
        if selected:
            self.cardeditor1.set_text(newtext1)
            self.cardeditor2.set_text(newtext2)
            self.cardeditor1.set_pixbuf(aimg)
            self.cardeditor2.set_pixbuf(bimg)
            self.cardeditor1.set_snd(asnd)
            self.cardeditor2.set_snd(bsnd)
            self.cardeditor1.set_speak(aspeak)
            self.cardeditor2.set_speak(bspeak)
            self._addbutton.set_sensitive(True)
        self._updatebutton.set_sensitive(selected)
        self._updatebutton_sensitive = selected

    def change_equal_pairs(self, widget, state):
        self.equal_pairs = state
        self.clean(None)

        if self.equal_pairs:
            if self.cardeditor2.parent:
                self.card_box.remove(self.cardeditor2)
        else:
            if not self.cardeditor2.parent:
                self.card_box.pack_start(self.cardeditor2, True, True, 0)

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

    def receive_font_signals(self, widget, font_name):
        if self.equal_pairs:
            self.emit('change-font', 1, font_name)
            self.emit('change-font', 2, font_name)
        else:
            if widget == self.cardeditor1:
                self.emit('change-font', 1, font_name)
            if widget == self.cardeditor2:
                self.emit('change-font', 2, font_name)

    def _update_buttom_status(self):
        if not self.equal_pairs:
            if (self._card1_has_text or self._card1_has_picture \
                    or self._card1_has_sound) and (self._card2_has_text
                                                   or self._card2_has_picture
                                                   or self._card2_has_sound):
                self._addbutton.set_sensitive(True)
                self._updatebutton.set_sensitive(self._updatebutton_sensitive)
            else:
                self._addbutton.set_sensitive(False)
                self._updatebutton.set_sensitive(False)
        else:
            if (self._card1_has_text or self._card1_has_picture \
                    or self._card1_has_sound):
                self._addbutton.set_sensitive(True)
                self._updatebutton.set_sensitive(self._updatebutton_sensitive)
            else:
                self._addbutton.set_sensitive(False)
                self._updatebutton.set_sensitive(False)

    def set_temp_folder(self, temp_folder):
        self.cardeditor1.temp_folder = temp_folder
        self.cardeditor2.temp_folder = temp_folder


class CardEditor(Gtk.EventBox):

    __gsignals__ = {
        'has-text': (GObject.SignalFlags.RUN_FIRST, None, [GObject.TYPE_PYOBJECT]),
        'has-picture': (GObject.SignalFlags.RUN_FIRST, None, [GObject.TYPE_PYOBJECT]),
        'has-sound': (GObject.SignalFlags.RUN_FIRST, None, [GObject.TYPE_PYOBJECT]),
        'change-font': (GObject.SignalFlags.RUN_FIRST, None, [GObject.TYPE_PYOBJECT]),
    }

    def __init__(self, editor_index):
        Gtk.EventBox.__init__(self)

        self.snd = None
        self.editor_index = editor_index
        self.temp_folder = None

        box = Gtk.VBox()
        box.props.spacing = theme.PAD
        box.props.border_width = theme.PAD

        self.previewlabel = Gtk.Label(label=_('Preview:'))
        self.previewlabel.set_alignment(0, 1)
        box.pack_start(self.previewlabel, False)

        self.card = svgcard.SvgCard(-1,
                 {'front_text': {'card_text': '',
                                 'text_color': '#ffffff'},
                  'front_border': {'fill_color': '#4c4d4f',
                                   'stroke_color': '#ffffff',
                                   'opacity': '1'}},
                None, theme.PAIR_SIZE, 1, '#c0c0c0')
        self.card.flip()
        card_align = Gtk.Alignment.new(.5, .5, 0, 0)
        card_align.add(self.card)
        box.pack_start(card_align, False)

        textlabel = Gtk.Label(label=_('Text:'))
        textlabel.set_alignment(0, 1)
        box.pack_start(textlabel, False)

        self.textentry = Gtk.Entry()
        self.textentry.connect('changed', self.update_text)
        box.pack_start(self.textentry, False)

        toolbar = RoundBox()

        browsepicture = ToolButton(
                icon_name='import_picture',
                tooltip=_('Insert picture'))
        toolbar.add(browsepicture)

        browsesound = ToolButton(
                icon_name='import_sound',
                tooltip=_('Insert sound'))
        toolbar.add(browsesound)

        browsepicture.connect('clicked', self._load_image)
        browsesound.connect('clicked', self._load_audio)

        if speak.espeak.supported:
            self.usespeak = ToggleToolButton(
                    named_icon='speak')
            self.usespeak.set_palette(SpeakPalette(self))
            toolbar.add(self.usespeak)
            self.usespeak.connect('toggled', self._usespeak_cb)
        else:
            self.usespeak = None

        self.font_combo = FontComboBox()
        self.id_font_changed = self.font_combo.connect("changed",
                self.__font_changed_cb)
        self.font_combo.set_font_name(model.DEFAULT_FONT)

        box.pack_start(self.font_combo, True, True, 0)
        box.pack_start(toolbar, True, True, 0)

        self.add(box)

    def __font_changed_cb(self, widget):
        font = widget.get_font_name()
        logging.error('Selected font %s', font)
        if font:
            self.card.change_font(font)
            self.emit('change-font', font)

    def set_font_name(self, font_name):
        self.font_combo.handler_block(self.id_font_changed)
        self.font_combo.set_font_name(font_name)
        self.font_combo.handler_unblock(self.id_font_changed)

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

    def get_speak(self):
        if self.usespeak is None:
            return None
        if self.usespeak.props.active:
            return self.usespeak.palette.face.status.voice.friendlyname

    def set_speak(self, value):
        if self.usespeak is None:
            return
        if value is None:
            self.usespeak.props.active = False
        else:
            try:
                self.usespeak.handler_block_by_func(self._usespeak_cb)
                self.usespeak.props.active = True
            finally:
                self.usespeak.handler_unblock_by_func(self._usespeak_cb)
            self.usespeak.palette.voices.resume(value)

    def get_pixbuf(self):
        return self.card.get_pixbuf()

    def set_pixbuf(self, pixbuf):
        self.card.set_pixbuf(pixbuf)

    def _load_image(self, widget):
        def load(jobject):
            index = jobject.file_path

            self.set_speak(None)

            pixbuf_t = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    index, theme.PAIR_SIZE - theme.PAD * 2,
                    theme.PAIR_SIZE - theme.PAD * 2)
            size = max(pixbuf_t.get_width(), pixbuf_t.get_height())
            pixbuf_z = GdkPixbuf.Pixbuf.new_from_file_at_size(
                'images/white.png', size, size)
            pixbuf_t.composite(pixbuf_z, 0, 0, pixbuf_t.get_width(),
                               pixbuf_t.get_height(), 0, 0, 1, 1,
                               GdkPixbuf.InterpType.BILINEAR, 255)
            self.card.set_pixbuf(pixbuf_z)
            _logger.debug('Picture Loaded: ' + index)
            self.emit('has-picture', True)
            del pixbuf_t
            del pixbuf_z

        chooser.pick(parent=self.get_toplevel(),
                     what=chooser.IMAGE,
                     cb=load)

    def _load_audio(self, widget):
        def load(jobject):
            index = jobject.file_path

            self.set_speak(None)

            dst = join(self.temp_folder, 'sounds', basename(index))
            shutil.copy(index, dst)
            self.set_snd(dst)
            icon_theme = Gtk.IconTheme.get_default()
            pixbuf_t = icon_theme.load_icon("audio-x-generic",
                                            style.XLARGE_ICON_SIZE, 0)
            self.card.set_pixbuf(pixbuf_t)
            self.emit('has-sound', True)
            _logger.debug('Audio Loaded: ' + dst)

        chooser.pick(parent=self.get_toplevel(),
                     what=chooser.AUDIO,
                     cb=load)

    def _usespeak_cb(self, button):
        self.card.change_speak(button.props.active)

        if not button.props.active:
            self.usespeak.palette.face.shut_up()
            return

        self.snd = None
        self.card.set_pixbuf(None)
        self.emit('has-sound', False)
        self.emit('has-picture', False)

        button.palette.face.say(self.get_text())

    def set_snd(self, snd):
        self.snd = snd

    def get_snd(self):
        return self.snd

    def get_font_name(self):
        return self.font_combo.get_font_name()

    def clean(self):
        self.textentry.set_text('')
        self.card.set_pixbuf(None)
        self.snd = None
        self.emit('has-text', False)
        self.emit('has-picture', False)
        self.emit('has-sound', False)
        if self.usespeak is not None and self.usespeak.palette is not None:
            self.usespeak.props.active = False
            self.usespeak.palette.face.shut_up()


class SpeakPalette(Palette):
    def __init__(self, editor):
        Palette.__init__(self, _('Pronounce text during tile flip'))

        self.face = speak.face.View()

        toolbar = Gtk.HBox()
        toolbar.modify_bg(Gtk.StateType.NORMAL, style.COLOR_BLACK.get_gdk_color())

        usespeak_play = ToolButton(icon_name='media-playback-start')
        usespeak_play.connect('clicked', lambda button:
                self.face.say(editor.get_text()))
        toolbar.pack_start(usespeak_play, False)

        self.voices = speak.widgets.Voices(self.face)
        toolbar.pack_start(ToolComboBox(self.voices, True, True, 0))

        toolbar.show_all()
        self.set_content(toolbar)
