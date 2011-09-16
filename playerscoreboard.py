#    Copyright (C) 2006, 2007, 2008 One Laptop Per Child
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

import svglabel
import logging
from os.path import join, dirname
from score import Score
import math

import theme

_logger = logging.getLogger('memorize-activity')


class PlayerScoreboard(gtk.EventBox):

    def __init__(self, nick, fill_color, stroke_color, score=0):
        gtk.EventBox.__init__(self)

        self.default_color = '#4c4d4f'
        self.selected_color = '#818286'
        self.current_color = '#4c4d4f'
        self.status = False
        self._score_width = 0
        self._score_cols = 0
        self._game_size = 16
        self.fill_color = fill_color
        self.stroke_color = stroke_color

        self.connect('size-allocate', self._allocate_cb)

        # Set table
        self.table = gtk.Table(2, 2, False)
        self.modify_bg(gtk.STATE_NORMAL,
                       gtk.gdk.color_parse(self.current_color))
        self.table.set_row_spacings(theme.PAD / 2)
        self.table.set_col_spacings(theme.PAD / 2)
        self.table.set_border_width(theme.PAD)

        # Score table
        self.score_table = gtk.Table()
        self.score_table.set_row_spacings(theme.PAD / 2)
        self.score_table.set_col_spacings(theme.PAD / 2)

        self.scores = []
        self.current_x = 0
        self.current_y = 0

        # Set buddy icon
        self.xo_buddy = join(dirname(__file__), 'images', 'stock-buddy.svg')
        self.icon = svglabel.SvgLabel(self.xo_buddy, fill_color, stroke_color,
                False, self.current_color, theme.BODY_WIDTH, theme.BODY_HEIGHT)

        # Set waiting buddy icon
        self.waiting_icon = svglabel.SvgLabel(self.xo_buddy, \
                self.default_color, '#ffffff', False, self.current_color,
                theme.BODY_WIDTH, theme.BODY_HEIGHT)

        # Set nick label
        self.nick = gtk.Label(nick)
        self.nick.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
        self.nick.set_alignment(0, 0.5)

        # Set message label
        self.msg = gtk.Label('Waiting for next game...')
        self.msg.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
        self.msg.set_alignment(0, 0.5)

        self.add(self.table)
        self.table.attach(self.icon, 0, 1, 0, 3, gtk.SHRINK, gtk.SHRINK)
        self.table.attach(self.nick, 1, 2, 0, 1)
        self.table.attach(self.score_table, 1, 2, 1, 2)

        if score != 0:
            for i_ in range(score):
                self.increase_score()

    def _allocate_cb(self, widget, allocation):
        self._score_width = allocation.width - theme.BODY_WIDTH \
                - theme.PAD * 2 - theme.PAD / 2
        self._score_cols = self._score_width / \
                (theme.SCORE_SIZE + theme.PAD / 2)
        self.change_game(self._game_size)

    def change_game(self, size):
        self._game_size = size
        if self._score_cols == 0:
            return

        rows = int(math.ceil(float(size / 2) / self._score_cols))
        self.score_table.resize(rows, self._score_cols)
        self.score_table.set_size_request(-1,
                (theme.SCORE_SIZE + theme.PAD / 2) * (rows) - theme.PAD / 2)

    def increase_score(self):
        if len(self.scores) == 0:
            # Cache the score icon
            score_label = Score(self.fill_color, self.stroke_color)
            score_pixbuf_unsel = score_label.get_pixbuf()
            score_pixbuf_sel = score_label.get_pixbuf_sel()
        else:
            score_pixbuf_unsel = None
            score_pixbuf_sel = None

        new_score = Score(self.fill_color, self.stroke_color,
                          score_pixbuf_sel, score_pixbuf_unsel, self.status)
        self.scores.append(new_score)
        new_score.show()
        self.score_table.attach(new_score, self.current_x, self.current_x + 1,
                self.current_y, self.current_y + 1, gtk.SHRINK, gtk.SHRINK)
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
        self.modify_bg(gtk.STATE_NORMAL,
                       gtk.gdk.color_parse(self.current_color))
        self.icon.set_background(self.current_color)
        for score in self.scores:
            score.set_selected(sel)
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
            self.table.remove(self.icon)
            self.table.attach(self.waiting_icon, 0, 1, 0, 2)
            if len(self.scores) == 0:
                self.table.attach(self.msg, 1, 2, 1, 2)
        else:
            self.table.remove(self.waiting_icon)
            self.table.attach(self.icon, 0, 1, 0, 2)
            self.table.remove(self.msg)
            if len(self.scores) == 0:
                self.table.remove(self.msg)
        self.queue_draw()

    def set_message(self, msg):
        self.msg.set_text(msg)
