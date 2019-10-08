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

from playerscoreboard import PlayerScoreboard


class Scoreboard(Gtk.EventBox):
    def __init__(self):
        Gtk.EventBox.__init__(self)
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse('#666666'))
        self._width = self.get_allocation().width
        self.players = {}
        self.current_buddy = None
        self.hbox = Gtk.HBox(False)
        self.hbox.set_homogeneous(True)
        self.hbox.set_valign(Gtk.Align.CENTER)
        self.add(self.hbox)
        self.show_all()

    def change_game(self, widget, data, grid):
        for buddy in list(self.players.keys()):
            self.players[buddy].change_game(len(grid))

    def add_buddy(self, widget, buddy, score):
        # FIXME: this breaks when the body is empty
        nick = buddy.props.nick
        stroke_color, fill_color = buddy.props.color.split(',')
        player = PlayerScoreboard(nick, fill_color, stroke_color, score)
        player.show()
        self.players[buddy] = player
        # remove widgets and add sorted
        for child in self.hbox.get_children():
            self.hbox.remove(child)
        for buddy in sorted(list(self.players.keys()),
                            key=lambda buddy: buddy.props.nick):
            p = self.players[buddy]
            self.hbox.pack_start(p, True, True, 0)

        if score == -1:
            player.set_wait_mode(True)
        self.show_all()

    def rem_buddy(self, widget, buddy):
        self.hbox.remove(self.players[buddy])
        del self.players[buddy]  # fix for self.players[id]

    def set_selected(self, widget, buddy):
        if self.current_buddy is not None:
            old = self.players[self.current_buddy]
            old.set_selected(False)
        self.current_buddy = buddy
        player = self.players[buddy]
        player.set_selected(True)

    def set_buddy_message(self, widget, buddy, msg):
        self.players[buddy].set_message(msg)

    def increase_score(self, widget, buddy):
        self.players[buddy].increase_score()

    def reset(self, widget):
        for buddy in list(self.players.keys()):
            self.players[buddy].reset()

    def set_wait_mode(self, widget, buddy, status):
        self.players[buddy].set_wait_mode(status)
