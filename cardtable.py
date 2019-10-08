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
from gi.repository import Pango

from sugar3.graphics import style

from card import Card
import os
import math

import logging

CARD_PAD = style.zoom(6)


class CardTable(Gtk.EventBox):

    __gsignals__ = {
        'card-flipped': (GObject.SignalFlags.RUN_FIRST,
                         None, [int, GObject.TYPE_PYOBJECT]),
        'card-highlighted': (GObject.SignalFlags.RUN_FIRST,
                             None, [int, GObject.TYPE_PYOBJECT]), }

    def __init__(self):
        Gtk.EventBox.__init__(self)
        self.data = None
        self.cards_data = None
        self._workspace_size = 0

        # set request size to 100x100 to skip first time sizing in _allocate_cb
        self.set_size_request(100, 100)
        self.connect('size-allocate', self._allocate_cb)

        self._background_color = '#BBBBBB'
        # Set table settings
        self.modify_bg(Gtk.StateType.NORMAL,
                       Gdk.color_parse(self._background_color))
        self.table = Gtk.Table()
        self.table.grab_focus()
        self.table.set_can_default(True)
        self.table.set_row_spacings(CARD_PAD)
        self.table.set_col_spacings(CARD_PAD)
        self.table.set_border_width(CARD_PAD)
        self.table.set_resize_mode(Gtk.ResizeMode.IMMEDIATE)
        self.table.set_halign(Gtk.Align.CENTER)
        self.table.set_valign(Gtk.Align.CENTER)
        self.set_property('child', self.table)
        self.load_message = Gtk.Label(label='Loading Game')
        self.load_message.modify_fg(Gtk.StateType.NORMAL,
                                    Gdk.color_parse('#ffffff'))
        self.load_message.modify_font(Pango.FontDescription('10'))
        self.load_message.show()
        self.first_load = True
        self.load_mode = False
        self.dict = None
        self.show_all()

    def resize(self, width, height, change=True):
        logging.debug('set size request %dx%d' % (width, height))
        self.set_size_request(width, height)
        self._workspace_size = min(width, height)
        if self.data:
            self.card_size = self.get_card_size(self.size)
            for child in self.table.get_children():
                child.resize(self.card_size)

    def _allocate_cb(self, widget, allocation):
        size = allocation.height
        width = Gdk.Screen.width()
        height = Gdk.Screen.height()
        size = min(width, height)
        if size == 100:
            # skip first time sizing
            return

        # do it once
        if self._workspace_size:
            return
        self.resize(width, height, change=False)

    def load_game(self, widget, data, grid):
        self.data = data
        self.cards_data = grid
        font_name1 = data['font_name1']
        font_name2 = data['font_name2']
        if self._workspace_size == 0:
            # widow is not allocated, thus postpone loading
            return

        self.size = int(math.ceil(math.sqrt(len(grid))))
        if self.size < 4:
            self.size = 4
        self.table.resize(self.size, self.size)
        self.card_size = self.get_card_size(self.size)
        self.cards = {}
        self.cd2id = {}
        self.id2cd = {}
        self.dict = {}
        self.selected_card = [0, 0]
        self.flipped_card = -1
        self.table_positions = {}

        # Build the table
        if data['divided'] == '1':
            text1 = str(self.data.get('face1', ''))
            text2 = str(self.data.get('face2', ''))
            background_color1 = style.Color('#4b4d4a')
            background_color2 = style.Color('#636564')
        else:
            text1 = str(self.data.get('face', ''))
            text2 = str(self.data.get('face', ''))
            background_color1 = style.Color('#4b4d4a')
            background_color2 = style.Color('#4b4d4a')
        x = 0
        y = 0
        identifier = 0

        # Don't want show robot face for art4apps games
        # even when playing a voice with text to speech (tts)
        try:
            show_robot = self.data['origin'] != 'art4apps'
        except KeyError:
            show_robot = True

        for card in self.cards_data:
            if card:
                if card.get('img', None):
                    image_path = os.path.join(
                        self.data['pathimg'], card['img'])
                else:
                    image_path = None
                props = {}
                props['front_text'] = {'card_text': card.get('char', ''),
                                       'speak': card.get('speak')}

                if card['ab'] == 'a':
                    props['back_text'] = {'card_text': text1}
                    font_name = font_name1
                    props['back'] = {'fill_color': background_color1,
                                     'stroke_color': background_color1}
                elif card['ab'] == 'b':
                    props['back_text'] = {'card_text': text2}
                    font_name = font_name2
                    props['back'] = {'fill_color': background_color2,
                                     'stroke_color': background_color2}

                card = Card(
                    identifier, props, image_path, self.card_size,
                    self._background_color, font_name, show_robot)
                card.connect('enter-notify-event', self.mouse_event, [x, y])
                card.set_events(Gdk.EventMask.TOUCH_MASK |
                                Gdk.EventMask.BUTTON_PRESS_MASK)
                card.connect('event', self.__event_cb, [x, y])
            else:
                card = Gtk.EventBox()
                card.modify_bg(
                    Gtk.StateType.NORMAL,
                    Gdk.color_parse(self._background_color))
                card.set_size_request(self.card_size, self.card_size)

            self.table_positions[(x, y)] = 1
            self.cd2id[card] = identifier
            self.id2cd[identifier] = card
            self.cards[(x, y)] = card
            self.dict[identifier] = (x, y)
            self.table.attach(card, x, x + 1, y, y + 1,
                              Gtk.AttachOptions.SHRINK,
                              Gtk.AttachOptions.SHRINK)

            x += 1
            if x == self.size:
                x = 0
                y += 1
            identifier += 1

        self.first_load = False
        if self.load_mode:
            self._set_load_mode(False)
        self.show_all()

    def change_game(self, widget, data, grid):
        if not self.first_load:
            for card in list(self.cards.values()):
                self.table.remove(card)
                del card
        self.load_game(None, data, grid)

    def get_card_size(self, size_table):
        x = (self._workspace_size + CARD_PAD * (size_table - 1)) // \
            size_table - CARD_PAD * 2
        return x

    def __event_cb(self, widget, event, coord):
        if event.type in (Gdk.EventType.TOUCH_BEGIN,
                          Gdk.EventType.BUTTON_PRESS):
            card = self.cards[coord[0], coord[1]]
            self.card_flipped(card)

    def mouse_event(self, widget, event, coord):
        card = self.cards[coord[0], coord[1]]
        identifier = self.cd2id.get(card)
        self.emit('card-highlighted', identifier, True)
        self.selected_card = (coord[0], coord[1])

    def key_press_event(self, widget, event):
        self.grab_focus()
        x = self.selected_card[0]
        y = self.selected_card[1]

        if event.keyval in (Gdk.KEY_Left, Gdk.KEY_KP_Left):
            if (x - 1, y) in self.table_positions:
                card = self.cards[x - 1, y]
                identifier = self.cd2id.get(card)
                if not (self.size == 5 and identifier == 12):
                    self.emit('card-highlighted', identifier, False)

        elif event.keyval in (Gdk.KEY_Right, Gdk.KEY_KP_Right):
            if (x + 1, y) in self.table_positions:
                card = self.cards[x + 1, y]
                identifier = self.cd2id.get(card)
                if not (self.size == 5 and identifier == 12):
                    self.emit('card-highlighted', identifier, False)

        elif event.keyval in (Gdk.KEY_Up, Gdk.KEY_KP_Up):
            if (x, y - 1) in self.table_positions:
                card = self.cards[x, y - 1]
                identifier = self.cd2id.get(card)
                if not (self.size == 5 and identifier == 12):
                    self.emit('card-highlighted', identifier, False)

        elif event.keyval in (Gdk.KEY_Down, Gdk.KEY_KP_Down):
            if (x, y + 1) in self.table_positions:
                card = self.cards[x, y + 1]
                identifier = self.cd2id.get(card)
                if not (self.size == 5 and identifier == 12):
                    self.emit('card-highlighted', identifier, False)

        elif event.keyval in (Gdk.KEY_space, Gdk.KEY_KP_Page_Down):
            card = self.cards[x, y]
            self.card_flipped(card)

    def card_flipped(self, card):
        identifer = self.cd2id[card]
        if not card.is_flipped():
            self.emit('card-flipped', identifer, False)

    def set_border(self, widget, identifer, stroke_color, fill_color):
        self.id2cd[identifer].set_border(stroke_color, fill_color,
                                         full_animation=True)

    def flop_card(self, widget, identifer):
        self.id2cd.get(identifer).flop()

    def flip_card(self, widget, identifer, full_animation):
        self.id2cd.get(identifer).flip(full_animation)

    def cement_card(self, widget, identifer):
        self.id2cd.get(identifer).cement()

    def highlight_card(self, widget, identifer, status):
        if self.dict is not None:
            self.selected_card = self.dict.get(identifer)
            self.id2cd.get(identifer).set_highlight(status)

    def reset(self, widget):
        for identifer in list(self.id2cd.keys()):
            self.id2cd[identifer].reset()

    def _set_load_mode(self, mode):
        if mode:
            self.remove(self.table)
            self.set_property('child', self.load_message)
        else:
            self.remove(self.load_message)
            self.set_property('child', self.table)
        self.load_mode = mode
        self.queue_draw()

    def load_msg(self, widget, msg):
        if not self.load_mode:
            self._set_load_mode(True)
        self.load_message.set_text(msg)
        self.queue_draw()
