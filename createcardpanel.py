# Copyright (C) 2006, 2007, 2008 One Laptop per Child
# Copyright (C) 2009 Simon Schampijer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gdk
from gi.repository import Gtk

from os.path import join, basename

import shutil
from gettext import gettext as _
from card import Card
import logging

from sugar3.activity import activity
from sugar3.graphics import style
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.icon import Icon
from sugar3.graphics.palette import Palette
from sugar3.graphics.toggletoolbutton import ToggleToolButton
from fontcombobox import FontButton
from port import chooser

import speak.face

PAIR_SIZE = min(Gdk.Screen.width() // 4, Gdk.Screen.height() // 3)


class CreateCardPanel(Gtk.EventBox):
    __gsignals__ = {
        'add-pair': (GObject.SignalFlags.RUN_FIRST, None,
                     10 * [GObject.TYPE_PYOBJECT]),
        'update-pair': (GObject.SignalFlags.RUN_FIRST, None,
                        8 * [GObject.TYPE_PYOBJECT]),
        'change-font': (GObject.SignalFlags.RUN_FIRST, None,
                        2 * [GObject.TYPE_PYOBJECT]),
        'pair-closed': (GObject.SignalFlags.RUN_FIRST,
                        None, []),
    }

    def __init__(self, game):
        def make_label(icon_name, label):
            label_box = Gtk.VBox()
            icon = Icon(icon_name=icon_name,
                        pixel_size=style.LARGE_ICON_SIZE)
            label_box.pack_start(icon, False, False, 0)
            label = Gtk.Label(label=label)
            label.modify_fg(Gtk.StateType.NORMAL,
                            style.COLOR_TOOLBAR_GREY.get_gdk_color())
            label_box.pack_start(label, True, True, 0)
            label_box.show_all()
            return label_box

        Gtk.EventBox.__init__(self)
        self._game = game
        self.equal_pairs = False
        self._updatebutton_sensitive = False
        self._card1_has_sound = False
        self._card2_has_sound = False

        # save buttons
        self._portrait = Gdk.Screen.width() < Gdk.Screen.height()

        if self._portrait:
            buttons_bar_orientation = Gtk.Orientation.HORIZONTAL
        else:
            buttons_bar_orientation = Gtk.Orientation.VERTICAL

        self._buttons_bar = Gtk.Box(orientation=buttons_bar_orientation)

        self._buttons_bar.props.border_width = 10
        self._buttons_bar.set_valign(Gtk.Align.CENTER)
        self._buttons_bar.set_halign(Gtk.Align.CENTER)

        self._addbutton = ToolButton(tooltip=_('Add as new pair'),
                                     sensitive=False)
        self._addbutton.set_icon_widget(
            make_label('pair-add', ' ' + _('Add')))
        self._addbutton.connect('clicked', self.emit_add_pair)
        self._buttons_bar.pack_start(self._addbutton, False, False, 0)

        self._updatebutton = ToolButton(tooltip=_('Update selected pair'),
                                        sensitive=False)
        self._updatebutton.set_icon_widget(
            make_label('pair-update', ' ' + _('Update')))
        self._updatebutton.connect('clicked', self.emit_update_pair)
        self._buttons_bar.pack_start(self._updatebutton, False, False, 0)

        self._removebutton = ToolButton(tooltip=_('Remove selected pair'),
                                        sensitive=False)
        self._removebutton.set_icon_widget(
            make_label('remove', ' ' + _('Remove')))
        self._removebutton.connect('clicked', self.emit_close)
        self._buttons_bar.pack_start(self._removebutton, False, False, 0)

        # Set card editors

        self.cardeditor1 = CardEditor(self._game, 1)
        self.cardeditor2 = CardEditor(self._game, 2)
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
        self.card_box.set_homogeneous(True)
        self.cardeditor1.set_halign(Gtk.Align.CENTER)
        self.cardeditor1.set_valign(Gtk.Align.CENTER)
        self.cardeditor2.set_halign(Gtk.Align.CENTER)
        self.cardeditor2.set_valign(Gtk.Align.CENTER)
        self.card_box.pack_start(self.cardeditor1, True, True, 0)
        self.card_box.pack_start(self.cardeditor2, True, True, 0)

        if self._portrait:
            main_box_orientation = Gtk.Orientation.VERTICAL
        else:
            main_box_orientation = Gtk.Orientation.HORIZONTAL
        self._main_box = Gtk.Box(orientation=main_box_orientation)
        self._main_box.pack_start(self.card_box, True, True, 0)
        self._main_box.pack_start(self._buttons_bar, True, True, 0)
        self.add(self._main_box)
        self.connect('size-allocate', self._allocate_cb)

        self.show_all()

    def _allocate_cb(self, widget, allocation):
        GLib.idle_add(self.update_orientation)

    def update_orientation(self):
        self._portrait = Gdk.Screen.width() < Gdk.Screen.height()
        if self._portrait:
            self._buttons_bar.props.orientation = Gtk.Orientation.HORIZONTAL
            self._main_box.props.orientation = Gtk.Orientation.VERTICAL
        else:
            self._buttons_bar.props.orientation = Gtk.Orientation.VERTICAL
            self._main_box.props.orientation = Gtk.Orientation.HORIZONTAL

    def update_font_combos(self, widget, data, grid):
        if 'font_name1' in data:
            self.cardeditor1.set_font_name(data['font_name1'])
            self.cardeditor1.card.change_font(data['font_name1'])
        if 'font_name2' in data:
            self.cardeditor2.set_font_name(data['font_name2'])
            self.cardeditor2.card.change_font(data['font_name2'])

    def emit_close(self, widget):
        self.emit('pair-closed')

    def emit_add_pair(self, widget):
        self._addbutton.set_sensitive(False)
        if self.equal_pairs:
            self.emit('add-pair', self.cardeditor1.get_text(),
                      self.cardeditor1.get_text(),
                      self.cardeditor1.get_image_path(),
                      self.cardeditor1.get_image_path(),
                      self.cardeditor1.get_snd(),
                      self.cardeditor1.get_snd(),
                      self.cardeditor1.get_speak(),
                      self.cardeditor1.get_speak(),
                      self.cardeditor1.get_font_name(),
                      self.cardeditor1.get_font_name())
        else:
            self.emit('add-pair', self.cardeditor1.get_text(),
                      self.cardeditor2.get_text(),
                      self.cardeditor1.get_image_path(),
                      self.cardeditor2.get_image_path(),
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
                      self.cardeditor1.get_image_path(),
                      self.cardeditor1.get_image_path(),
                      self.cardeditor1.get_snd(),
                      self.cardeditor1.get_snd(),
                      self.cardeditor1.get_speak(),
                      self.cardeditor1.get_speak())
        else:
            self.emit('update-pair', self.cardeditor1.get_text(),
                      self.cardeditor2.get_text(),
                      self.cardeditor1.get_image_path(),
                      self.cardeditor2.get_image_path(),
                      self.cardeditor1.get_snd(),
                      self.cardeditor2.get_snd(),
                      self.cardeditor1.get_speak(),
                      self.cardeditor2.get_speak())
        self.clean(None)

    def pair_selected(self, widget, selected, newtext1, newtext2,
                      aimage_path, bimage_path, asnd, bsnd, aspeak, bspeak):
        if selected:
            self.cardeditor1.set_text(newtext1)
            self.cardeditor2.set_text(newtext2)
            self.cardeditor1.set_image_path(aimage_path)
            self.cardeditor2.set_image_path(bimage_path)
            self.cardeditor1.set_snd(asnd)
            self.cardeditor2.set_snd(bsnd)
            self.cardeditor1.set_speak(aspeak)
            self.cardeditor2.set_speak(bspeak)
            self._addbutton.set_sensitive(True)
        self._updatebutton.set_sensitive(selected)
        self._updatebutton_sensitive = selected
        self._removebutton.set_sensitive(selected)

    def change_equal_pairs(self, widget, state):
        self.equal_pairs = state
        self.clean(None)

        if self.equal_pairs:
            if self.cardeditor2.get_parent():
                self.card_box.remove(self.cardeditor2)
        else:
            if not self.cardeditor2.get_parent():
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
            if (self._card1_has_text or self._card1_has_picture or
                self._card1_has_sound) and (self._card2_has_text or
                                            self._card2_has_picture or
                                            self._card2_has_sound):
                self._addbutton.set_sensitive(True)
                self._updatebutton.set_sensitive(self._updatebutton_sensitive)
            else:
                self._addbutton.set_sensitive(False)
                self._updatebutton.set_sensitive(False)
        else:
            if (self._card1_has_text or self._card1_has_picture or
                    self._card1_has_sound):
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
        'has-text': (GObject.SignalFlags.RUN_FIRST, None,
                     [GObject.TYPE_PYOBJECT]),
        'has-picture': (GObject.SignalFlags.RUN_FIRST, None,
                        [GObject.TYPE_PYOBJECT]),
        'has-sound': (GObject.SignalFlags.RUN_FIRST, None,
                      [GObject.TYPE_PYOBJECT]),
        'change-font': (GObject.SignalFlags.RUN_FIRST, None,
                        [GObject.TYPE_PYOBJECT]),
    }

    def __init__(self, game, editor_index):
        Gtk.EventBox.__init__(self)
        self._game = game
        self.snd = None
        self.editor_index = editor_index
        self.temp_folder = None

        box = Gtk.Grid()
        box.set_column_spacing(style.DEFAULT_SPACING)
        box.set_row_spacing(style.DEFAULT_SPACING)
        box.props.margin = style.DEFAULT_SPACING

        self.card = Card(
            -1, {'front_text': {'card_text': '',
                                'text_color': style.Color('#ffffff')}},
            None, PAIR_SIZE, '#c0c0c0')
        self.card.flip()
        card_align = Gtk.Alignment.new(.5, .5, 0, 0)
        card_align.add(self.card)
        box.attach(card_align, 0, 0, 1, 1)

        self.textentry = Gtk.Entry()
        self.textentry.connect('changed', self.update_text)
        self.textentry.set_valign(Gtk.Align.START)
        box.attach(self.textentry, 0, 1, 1, 1)

        toolbar = Gtk.VBox()
        toolbar.set_valign(Gtk.Align.CENTER)

        browsepicture = ToolButton(icon_name='import_picture',
                                   tooltip=_('Insert picture'))
        toolbar.add(browsepicture)

        browsesound = ToolButton(icon_name='import_sound',
                                 tooltip=_('Insert sound'))
        toolbar.add(browsesound)

        browsepicture.connect('clicked', self._load_image)
        browsesound.connect('clicked', self._load_audio)

        self.usespeak = ToggleToolButton(icon_name='speak')
        self.usespeak.set_palette(SpeakPalette(self))
        toolbar.add(self.usespeak)
        self.usespeak.connect('toggled', self._usespeak_cb)

        self.fontbutton = FontButton()
        toolbar.add(self.fontbutton)
        self.id_font_changed = self.fontbutton.connect(
            'changed', self.__font_changed_cb)
        box.attach(toolbar, 1, 0, 1, 2)

        self.add(box)

    def __font_changed_cb(self, widget):
        font = widget.get_font_name()
        if font:
            self.card.change_font(font)
            self.emit('change-font', font)

    def set_font_name(self, font_name):
        self.fontbutton.handler_block(self.id_font_changed)
        self.fontbutton.set_font_name(font_name)
        self.fontbutton.handler_unblock(self.id_font_changed)

    def update_text(self, entry):
        self.card.change_text(entry.get_text())
        if len(entry.get_text()) == 0:
            self.emit('has-text', False)
        else:
            self.emit('has-text', True)

    def get_text(self):
        return self.textentry.get_text()

    def set_text(self, newtext):
        if newtext is None:
            newtext = ''
        self.textentry.set_text(newtext)

    def get_speak(self):
        if self.usespeak is None:
            return None
        active = 'True' if self.usespeak.props.active else 'False'
        return active

    def set_speak(self, active):
        if self.usespeak is None:
            return
        self.usespeak.handler_block_by_func(self._usespeak_cb)
        self.usespeak.props.active = active == 'True'
        self.usespeak.handler_unblock_by_func(self._usespeak_cb)

    def get_image_path(self):
        return self.card.get_image_path()

    def set_image_path(self, image_path):
        self.card.set_image_path(image_path)
        self.emit('has-picture', True)

    def _load_image(self, widget):
        def load(jobject):
            origin_path = jobject.file_path
            self._game.model.mark_modified()
            self._game.model.create_temp_directories()
            destination_path = join(self._game.model.data['pathimg'],
                                    basename(origin_path))
            shutil.copy(origin_path, destination_path)
            self.set_speak(False)
            self.card.set_image_path(destination_path)
            logging.debug('Picture Loaded: %s', destination_path)
            self.emit('has-picture', True)

        chooser.pick(parent=self.get_toplevel(),
                     what=chooser.IMAGE,
                     cb=load)

    def _load_audio(self, widget):
        def load(jobject):
            origin_path = jobject.file_path
            self.set_speak(False)
            self._game.model.mark_modified()
            self._game.model.create_temp_directories()
            destination_path = join(self._game.model.data['pathsnd'],
                                    basename(origin_path))
            shutil.copy(origin_path, destination_path)
            self.set_snd(destination_path)
            logging.debug('Audio Loaded: %s', destination_path)

            # add a icon too
            sound_icon_path = join(activity.get_bundle_path(),
                                   'icons/sounds.svg')
            destination_path = join(self._game.model.data['pathimg'],
                                    'sounds.svg')
            shutil.copy(sound_icon_path, destination_path)

            self.card.set_image_path(destination_path)
            self.emit('has-sound', True)

        chooser.pick(parent=self.get_toplevel(),
                     what=chooser.AUDIO,
                     cb=load)

    def _usespeak_cb(self, button):
        self.card.change_speak(button.props.active)

        if not button.props.active:
            self.usespeak.palette.face.shut_up()
            return

        self.snd = None
        self.emit('has-sound', False)
        self.emit('has-picture', False)

        button.palette.face.say(self.get_text())

    def set_snd(self, snd):
        self.snd = snd

    def get_snd(self):
        return self.snd

    def get_font_name(self):
        return self.fontbutton.get_font_name()

    def clean(self):
        self.textentry.set_text('')
        self.card.set_image_path(None)
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
        toolbar.modify_bg(Gtk.StateType.NORMAL,
                          style.COLOR_BLACK.get_gdk_color())

        usespeak_play = ToolButton(icon_name='media-playback-start')
        usespeak_play.connect('clicked', lambda button:
                              self.face.say(editor.get_text()))
        toolbar.pack_start(usespeak_play, False, False, 0)

        toolbar.show_all()
        self.set_content(toolbar)
