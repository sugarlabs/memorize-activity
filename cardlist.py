# Copyright (C) 2006, 2007, 2008 One Laptop per Child
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

from gi.repository import GObject
from gi.repository import Gdk
from gi.repository import Gtk

from card import Card
import logging
from os.path import join, basename

from model import Pair

from sugar3.graphics import style
from sugar3 import profile

PAIR_SIZE = min(Gdk.Screen.width() // 7, Gdk.Screen.height() // 5)
user_color = profile.get_color()


class CardList(Gtk.EventBox):

    __gsignals__ = {
        'pair-selected': (GObject.SignalFlags.RUN_FIRST,
                          None, 9 * [GObject.TYPE_PYOBJECT]),
        'update-create-toolbar': (GObject.SignalFlags.RUN_FIRST,
                                  None, 3 * [GObject.TYPE_PYOBJECT]),
    }

    def __init__(self):
        Gtk.EventBox.__init__(self)
        self.pairs = []
        self.current_pair = None
        self.current_game_key = None
        self.model = None
        self.pair_list_modified = False
        self.game_loaded = False

        self.hbox = Gtk.HBox(False)

        fill_box = Gtk.Label()
        fill_box.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse('#d7d7d7'))
        fill_box.show()
        self.hbox.pack_end(fill_box, True, True, 0)

        self._scroll = Gtk.ScrolledWindow()
        self._scroll.set_policy(Gtk.PolicyType.AUTOMATIC,
                                Gtk.PolicyType.AUTOMATIC)
        self._scroll.add_with_viewport(self.hbox)
        self._scroll.set_border_width(0)
        self._scroll.get_child().modify_bg(Gtk.StateType.NORMAL,
                                           Gdk.color_parse('#d7d7d7'))
        self.add(self._scroll)
        self.set_size_request(-1, PAIR_SIZE * 2 + style.DEFAULT_SPACING * 4)
        self.show_all()

    def load_game(self, game):
        if self.game_loaded:
            return
        self.get_window().freeze_updates()
        self.model = game.model
        self.current_game_key = self.model.data['game_file']
        font_name1 = self.model.data['font_name1']
        font_name2 = self.model.data['font_name2']
        game_pairs = self.model.pairs
        self.clean_list(load=True)
        for key in game_pairs:
            if game_pairs[key].props.aimg is not None:
                aimg_path = join(self.model.data['pathimg'],
                                 game_pairs[key].props.aimg)
            else:
                aimg_path = None

            if game_pairs[key].props.bimg is not None:
                bimg_path = join(self.model.data['pathimg'],
                                 game_pairs[key].props.bimg)
            else:
                bimg_path = None

            if game_pairs[key].props.asnd is not None:
                asnd = join(self.model.data['pathsnd'],
                            game_pairs[key].props.asnd)
            else:
                asnd = None

            if game_pairs[key].props.bsnd is not None:
                bsnd = join(self.model.data['pathsnd'],
                            game_pairs[key].props.bsnd)
            else:
                bsnd = None

            self.add_pair(
                None, game_pairs[key].props.achar,
                game_pairs[key].props.bchar, aimg_path, bimg_path, asnd, bsnd,
                game_pairs[key].props.aspeak, game_pairs[key].props.bspeak,
                font_name1, font_name2, False, load=True)
        self.get_window().thaw_updates()
        self.emit('update-create-toolbar', self.model.data['name'],
                  self.model.data['equal_pairs'],
                  self.model.data['divided'])
        self.game_loaded = True

    def update_model(self, game_model):
        game_model.pairs = {}

        for pair in range(len(self.pairs)):
            pair_card = Pair()
            # achar
            achar = self.pairs[pair].get_text(1)
            if achar != '':
                pair_card.set_property('achar', achar)

            # bchar
            bchar = self.pairs[pair].get_text(2)
            if bchar != '':
                pair_card.set_property('bchar', bchar)

            # aspeak
            aspeak = self.pairs[pair].get_speak(1)
            pair_card.set_property('aspeak', aspeak)

            # bspeak
            bspeak = self.pairs[pair].get_speak(2)
            pair_card.set_property('bspeak', bspeak)

            # aimg
            aimg = self.pairs[pair].get_image_path(1)
            if aimg is not None:
                aimgfile = self.pairs[pair].get_image_path(1)
                pair_card.set_property('aimg', basename(aimgfile))
            # bimg
            bimg = self.pairs[pair].get_image_path(2)
            if bimg is not None:
                bimgfile = self.pairs[pair].get_image_path(2)
                pair_card.set_property('bimg', basename(bimgfile))
            # asnd
            asnd = self.pairs[pair].get_sound(1)
            logging.debug('update_model asnd %s', asnd)
            if asnd is not None:
                pair_card.set_property('asnd', basename(asnd))
            # bsnd
            bsnd = self.pairs[pair].get_sound(2)
            logging.debug('update_model bsnd %s', bsnd)
            if bsnd is not None:
                pair_card.set_property('bsnd', basename(bsnd))

            game_model.pairs[pair] = pair_card
        self.pair_list_modified = False

    def clean_list(self, button=None, load=False):
        if button is not None:
            self.current_game_key = None
        list(map(lambda x: self.hbox.remove(x), self.pairs))
        del self.pairs
        self.pairs = []
        if not load:
            self.pair_list_modified = True
            self.model.mark_modified()

    def add_pair(self, widget, achar, bchar, aimg_path, bimg_path, asnd, bsnd,
                 aspeak, bspeak, font_name1, font_name2,
                 show=True, load=False):
        pair = CardPair(achar, bchar, aimg_path, bimg_path, asnd, bsnd,
                        aspeak, bspeak, font_name1, font_name2)
        self.hbox.pack_end(pair, False, True, 0)
        self.pairs.append(pair)
        pair.connect('pair-selected', self.set_selected)
        if not load:
            self.model.mark_modified()
            self.pair_list_modified = True
            adj = self._scroll.get_vadjustment()
            adj.set_value(adj.get_lower())
        if show:
            self.show_all()

    def change_font(self, widget, group, font_name):
        for pair in self.pairs:
            pair.change_font(group, font_name)
        if group == 1:
            self.model.data['font_name1'] = font_name
        if group == 2:
            self.model.data['font_name2'] = font_name
        self.model.mark_modified()

    def rem_current_pair(self, widget):
        self.hbox.remove(self.current_pair)
        self.pairs.remove(self.current_pair)
        self.current_pair = None
        self.model.mark_modified()
        self.emit('pair-selected', False, None, None, None, None, None, None,
                  False, False)

    def set_selected(self, widget, event):
        if self.current_pair is not None:
            current_pair = self.current_pair
            current_pair.set_selected(False)
        self.current_pair = widget
        widget.set_selected(True)
        self.emit('pair-selected', True,
                  self.current_pair.get_text(1),
                  self.current_pair.get_text(2),
                  self.current_pair.get_image_path(1),
                  self.current_pair.get_image_path(2),
                  self.current_pair.get_sound(1),
                  self.current_pair.get_sound(2),
                  self.current_pair.get_speak(1),
                  self.current_pair.get_speak(2))

    def update_selected(self, widget, newtext1, newtext2, aimg_path, bimg_path,
                        asnd, bsnd, aspeak, bspeak):
        self.current_pair.change_text(newtext1, newtext2)
        self.current_pair.change_image_path(aimg_path, bimg_path)
        self.current_pair.change_sound(asnd, bsnd)
        self.current_pair.change_speak(aspeak, bspeak)
        self.model.mark_modified()
        self.pair_list_modified = False


class CardPair(Gtk.EventBox):

    __gsignals__ = {
        'pair-selected': (GObject.SignalFlags.RUN_FIRST,
                          None, [GObject.TYPE_PYOBJECT]),
    }

    def __init__(self, text1, text2=None, aimg_path=None, bimg_path=None,
                 asnd=None, bsnd=None, aspeak=None, bspeak=None,
                 font_name1=None, font_name2=None):
        Gtk.EventBox.__init__(self)
        self.bg_color = '#d7d7d7'
        self._stroke_color = '#ffffff'
        self._fill_color = '#4c4d4f'

        self.asnd = asnd
        self.bsnd = bsnd

        self.current_game_key = None

        row = Gtk.VBox()
        row.props.margin_left = style.DEFAULT_SPACING
        row.props.margin_right = style.DEFAULT_SPACING

        self.bcard1 = Card(
            -1, {'front_text': {'card_text': text1,
                                'speak': aspeak,
                                'text_color': style.Color('#ffffff')},
                 'front': {'fill_color': style.Color(self._fill_color),
                           'stroke_color': style.Color(self._stroke_color)}},
            aimg_path, PAIR_SIZE, self.bg_color, font_name1)
        self.bcard1.flip()
        self.bcard1.set_valign(Gtk.Align.CENTER)
        row.pack_start(self.bcard1, True, True, 0)

        self.bcard2 = Card(
            -1, {'front_text': {'card_text': text2,
                                'speak': bspeak,
                                'text_color': style.Color('#ffffff')},
                 'front': {'fill_color': style.Color(self._fill_color),
                           'stroke_color': style.Color(self._stroke_color)}},
            bimg_path, PAIR_SIZE, self.bg_color, font_name2)
        self.bcard2.flip()
        self.bcard2.set_valign(Gtk.Align.CENTER)
        row.pack_start(self.bcard2, True, True, 0)
        self.connect('button-press-event', self.emit_selected)
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(self.bg_color))
        self.add(row)
        self.show_all()

    def emit_selected(self, widget, event):
        self.emit('pair-selected', self)

    def set_selected(self, status):
        if not status:
            stroke_color = self._stroke_color
            fill_color = self._fill_color
        else:
            stroke_color = user_color.get_stroke_color()
            fill_color = user_color.get_fill_color()

        self.bcard1.set_border(stroke_color, fill_color)
        self.bcard2.set_border(stroke_color, fill_color)

    def change_image_path(self, aimage_path, bimage_path):
        self.bcard1.set_image_path(aimage_path)
        self.bcard2.set_image_path(bimage_path)

    def change_text(self, text1, text2):
        self.bcard1.change_text(text1)
        self.bcard2.change_text(text2)

    def change_sound(self, asnd, bsnd):
        self.asnd = asnd
        self.bsnd = bsnd

    def change_font(self, card, font_name):
        if card == 1:
            self.bcard1.change_font(font_name)
        else:
            self.bcard2.change_font(font_name)

    def get_text(self, card):
        if card == 1:
            return self.bcard1.get_text()
        else:
            return self.bcard2.get_text()

    def change_speak(self, aspeak, bspeak):
        self.bcard1.change_speak(aspeak)
        self.bcard2.change_speak(bspeak)

    def get_speak(self, card):
        if card == 1:
            return self.bcard1.get_speak()
        else:
            return self.bcard2.get_speak()

    def get_image_path(self, card):
        if card == 1:
            return self.bcard1.get_image_path()
        else:
            return self.bcard2.get_image_path()

    def get_sound(self, card):
        if card == 1:
            return self.asnd
        else:
            return self.bsnd
