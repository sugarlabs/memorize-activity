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

from gi.repository import Gdk
from gi.repository import Gtk

from sugar3.graphics.icon import Icon
from sugar3.graphics import style

import math


class PlayerScoreboard(Gtk.EventBox):

    def __init__(self, nick, fill_color, stroke_color, score=0):
        Gtk.EventBox.__init__(self)

        self.default_color = '#666666'
        self.selected_color = '#818286'
        self.current_color = '#666666'
        self.status = False
        self._score_width = 0
        self._score_cols = 0
        self._game_size = 16
        self.fill_color = fill_color
        self.stroke_color = stroke_color

        self.connect('size-allocate', self._allocate_cb)

        # Set table
        self.table = Gtk.Table(2, 2, False)
        self.modify_bg(Gtk.StateType.NORMAL,
                       Gdk.color_parse(self.current_color))
        self.table.set_row_spacings(0)
        self.table.set_col_spacings(0)
        self.table.set_border_width(style.DEFAULT_SPACING // 2)

        # Score table
        self.score_table = Gtk.Table()
        self.score_table.set_row_spacings(style.DEFAULT_SPACING // 2)
        self.score_table.set_col_spacings(style.DEFAULT_SPACING // 2)

        self.scores = []
        self.current_x = 0
        self.current_y = 0

        # Set buddy icon
        self.icon = Icon(icon_name='computer-xo',
                         pixel_size=style.STANDARD_ICON_SIZE)
        self.icon.set_fill_color(fill_color)
        self.icon.set_stroke_color(stroke_color)

        # Set nick label
        self.nick = Gtk.Label(label=nick)
        self.nick.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse('#ffffff'))
        self.nick.set_alignment(0, 0.5)

        # Set message label
        self.msg = Gtk.Label(label='Waiting for next game...')
        self.msg.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse('#ffffff'))
        self.msg.set_alignment(0, 0.5)

        self.add(self.table)
        self.table.attach(self.icon, 0, 1, 0, 3, Gtk.AttachOptions.SHRINK,
                          Gtk.AttachOptions.SHRINK)
        self.table.attach(self.nick, 1, 2, 0, 1)
        self.table.attach(self.score_table, 1, 2, 1, 2)

        if score != 0:
            for i_ in range(score):
                self.increase_score()

    def _allocate_cb(self, widget, allocation):
        self._score_width = allocation.width - style.STANDARD_ICON_SIZE \
            - style.DEFAULT_SPACING * 2 - style.DEFAULT_SPACING // 2
        self._score_cols = self._score_width // \
            (style.SMALL_ICON_SIZE + style.DEFAULT_SPACING // 2)
        self.change_game(self._game_size)

    def change_game(self, size):
        self._game_size = size
        if self._score_cols == 0:
            return

        rows = int(math.ceil(size / (2 * self._score_cols)))
        self.score_table.resize(rows, self._score_cols)
        self.score_table.set_size_request(
            -1,
            (style.SMALL_ICON_SIZE + style.DEFAULT_SPACING // 2) * rows -
            style.DEFAULT_SPACING // 2)

    def increase_score(self):
        new_score = Icon(icon_name='score',
                         pixel_size=style.SMALL_ICON_SIZE)
        new_score.set_fill_color(self.fill_color)
        new_score.set_stroke_color(self.stroke_color)

        self.scores.append(new_score)
        new_score.show()
        self.score_table.attach(
            new_score, self.current_x, self.current_x + 1,
            self.current_y, self.current_y + 1, Gtk.AttachOptions.SHRINK,
            Gtk.AttachOptions.SHRINK)
        self.current_x += 1
        if self.current_x == self._score_cols:
            self.current_x = 0
            self.current_y += 1
        self.queue_draw()

    def set_selected(self, sel):
        self.status = sel
        if sel:
            self.current_color = self.selected_color
        else:
            self.current_color = self.default_color
        self.modify_bg(Gtk.StateType.NORMAL,
                       Gdk.color_parse(self.current_color))
        self.icon.set_fill_color(self.fill_color)
        for score in self.scores:
            score.set_fill_color(self.fill_color)
        self.queue_draw()

    def reset(self):
        for score in self.scores:
            self.score_table.remove(score)
        self.current_x = 0
        self.current_y = 0
        del self.scores
        self.scores = []
        self.queue_draw()

    def set_wait_mode(self, status):
        if status:
            self.icon.set_fill_color('#ffffff')
            if len(self.scores) == 0:
                self.table.attach(self.msg, 1, 2, 1, 2)
        else:
            self.icon.set_fill_color(self.fill_color)
            if len(self.scores) == 0:
                self.table.remove(self.msg)
        self.queue_draw()

    def set_message(self, msg):
        self.msg.set_text(msg)
