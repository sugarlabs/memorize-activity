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

import logging
from gi.repository import GLib
from gi.repository import GObject
from os.path import join

from gettext import gettext as _

from model import Model
from audio import Audio

FLOP_BACK_TIMEOUT = 2000


class MemorizeGame(GObject.GObject):

    __gsignals__ = {
        'reset_scoreboard': (GObject.SignalFlags.RUN_FIRST, None, []),
        'reset_table': (GObject.SignalFlags.RUN_FIRST, None, []),
        'load_mode': (GObject.SignalFlags.RUN_FIRST, None,
                      [GObject.TYPE_PYOBJECT]),
        'load_game': (GObject.SignalFlags.RUN_FIRST, None,
                      2 * [GObject.TYPE_PYOBJECT]),
        'change_game': (GObject.SignalFlags.RUN_FIRST, None,
                        2 * [GObject.TYPE_PYOBJECT]),
        'change_game_signal': (GObject.SignalFlags.RUN_FIRST, None,
                               5 * [GObject.TYPE_PYOBJECT]),
        'set-border': (GObject.SignalFlags.RUN_FIRST, None,
                       3 * [GObject.TYPE_PYOBJECT]),
        'flip-card': (GObject.SignalFlags.RUN_FIRST, None, [int, bool]),
        'flip-card-signal': (GObject.SignalFlags.RUN_FIRST, None, [int]),
        'cement-card': (GObject.SignalFlags.RUN_FIRST, None, [int]),
        'flop-card': (GObject.SignalFlags.RUN_FIRST, None, [int]),
        'highlight-card': (GObject.SignalFlags.RUN_FIRST, None,
                           2 * [GObject.TYPE_PYOBJECT]),
        'add_buddy': (GObject.SignalFlags.RUN_FIRST, None,
                      2 * [GObject.TYPE_PYOBJECT]),
        'rem_buddy': (GObject.SignalFlags.RUN_FIRST, None,
                      [GObject.TYPE_PYOBJECT]),
        'increase-score': (GObject.SignalFlags.RUN_FIRST, None,
                           [GObject.TYPE_PYOBJECT]),
        'wait_mode_buddy': (GObject.SignalFlags.RUN_FIRST, None,
                            2 * [GObject.TYPE_PYOBJECT]),
        'msg_buddy': (GObject.SignalFlags.RUN_FIRST, None,
                      2 * [GObject.TYPE_PYOBJECT]),
        'change-turn': (GObject.SignalFlags.RUN_FIRST, None,
                        [GObject.TYPE_PYOBJECT]), }

    def __init__(self):
        GObject.GObject.__init__(self)
        self.myself = None
        self.players_score = {}
        self.players = []
        self.waiting_players = []
        self.current_player = None
        self.last_flipped = -1
        self.last_highlight = 1
        self._flop_card_timeout = -1
        self.sentitive = True

        self.model = Model()
        self.flip_block = False
        self._flop_cards = None

        self.audio = Audio()
        self._audio_play_finished_id = 0

    def load_game(self, game_name, size, mode):
        self.set_load_mode('Loading game')
        if self.model.read(game_name) == 0:
            logging.debug('load_game set is_demo mode %s', mode)
            self.model.is_demo = (mode == 'demo')
            self.model.def_grid(size)
            self.model.data['running'] = 'False'
            self.model.data['mode'] = mode
            logging.debug(' Read setup file %r: %r ',
                          game_name, self.model.grid)
            self.emit('load_game', self.model.data, self.model.grid)
        else:
            logging.error(' Reading setup file %s', game_name)

    def load_remote(self, grid, data, mode, signal=False):
        self.set_load_mode(_('Loading game...'))
        self.model.grid = grid
        self.model.data = data
        self.model.data['mode'] = mode
        self.emit('reset_scoreboard')
        if not signal:
            self.emit('change_game_signal', mode, self.get_grid(),
                      self.model.data, self.waiting_players,
                      self.model.data['game_file'])
        self.emit('change_game', self.model.data, self.get_grid())
        for buddy in self.players:
            self.players_score[buddy] = 0
        self.current_player = None
        self.last_flipped = -1
        self.last_highlight = 1
        self.change_turn()
        self.model.data['running'] = 'False'

        for card in self.model.grid:
            if len(card) > 0:
                if card['state'] == '1':
                    self.emit('flip-card', self.model.grid.index(card), False)
                    self.last_flipped = self.model.grid.index(card)
                elif card['state'] != '0':
                    stroke_color, fill_color = card['state'].split(',')
                    self.emit('flip-card', self.model.grid.index(card), False)
                    self.emit('set-border', self.model.grid.index(card),
                              stroke_color, fill_color)
            else:
                continue
        logging.debug('load_remote set is_demo mode %s', mode)
        if mode != 'reset':
            self.model.is_demo = (mode == 'demo')

    def add_buddy(self, buddy, score=0):
        logging.debug('Buddy %r was added to game', buddy.props.nick)
        self.players.append(buddy)
        def key(a):
            return a.props.nick
        self.players = sorted(self.players, key=key)
        self.players_score[buddy] = score
        self.emit('add_buddy', buddy, score)
        logging.debug(str(buddy))

        if self.current_player is None:
            self.current_player = buddy
            self.change_turn()

    def rem_buddy(self, buddy):
        logging.debug('Buddy %r was removed from game', buddy.props.nick)
        if self.current_player == buddy and len(self.players) >= 2:
            if self.last_flipped != -1:
                self.emit('flop-card', self.last_flipped)
                self.model.grid[self.last_flipped]['state'] = '0'
                self.last_flipped = -1
            self.change_turn()
        index = self.players.index(buddy)
        del self.players[index]
        del (self.players_score[buddy])
        self.emit('rem_buddy', buddy)

    def buddy_message(self, buddy, text):
        self.emit('msg_buddy', buddy, text)

    def update_turn(self):
        self.set_sensitive(self.current_player == self.myself)
        self.emit('change-turn', self.current_player)

    def change_turn(self):
        if len(self.players) <= 1:
            self.current_player = self.players[0]
        if self.current_player is None:
            self.current_player = self.players[0]
        elif self.current_player == self.players[-1]:
            self.current_player = self.players[0]
        else:
            next_player = self.players.index(self.current_player) + 1
            self.current_player = self.players[next_player]
        self.update_turn()

    def card_flipped(self, widget, identifier, signal=False):
        self.model.count = self.model.count + 1

        # Check if is my turn
        if (not self.sentitive and not signal) or \
                self.last_flipped == identifier:
            return

        # Handle groups if needed
        if self.model.data.get('divided') == '1':
            if self.last_flipped == -1 and identifier \
                    >= (len(self.model.grid) // 2):
                return
            if self.last_flipped != -1 and identifier \
                    < (len(self.model.grid) // 2):
                return

        # do not process flips when flipping back
        if self.flip_block:
            return
        else:
            self.flip_block = True

        self.model.data['running'] = 'True'

        def flip_card(full_animation):
            self.emit('flip-card', identifier, full_animation)
            if not signal:
                self.emit('flip-card-signal', identifier)

        snd = self.model.grid[identifier].get('snd', None)
        if snd is not None:
            sound_file = join(self.model.data.get('pathsnd'), snd)

            if self._audio_play_finished_id != 0:
                self.audio.disconnect(self._audio_play_finished_id)

            self.audio.play(sound_file)

        # First card case
        if self.last_flipped == -1:
            flip_card(full_animation=True)

            self.last_flipped = identifier
            self.model.grid[identifier]['state'] = '1'
            self.flip_block = False

        # Second card case
        else:
            # Pair matched
            pair_key_1 = self.model.grid[self.last_flipped]['pairkey']
            pair_key_2 = self.model.grid[identifier]['pairkey']

            if pair_key_1 == pair_key_2:
                if not signal:
                    self.emit('flip-card-signal', identifier)

                stroke_color, fill_color = \
                    self.current_player.props.color.split(',')
                self.emit('set-border', identifier, stroke_color, fill_color)
                self.emit('set-border', self.last_flipped,
                          stroke_color, fill_color)

                self.increase_point(self.current_player)
                self.model.grid[identifier]['state'] = \
                    self.current_player.props.color
                self.model.grid[self.last_flipped]['state'] = \
                    self.current_player.props.color
                self.flip_block = False

                self.emit('cement-card', identifier)
                self.emit('cement-card', self.last_flipped)

            # Pair didn't match
            else:
                flip_card(full_animation=True)

                self.model.grid[identifier]['state'] = '1'
                self.set_sensitive(False)
                self._flop_cards = (identifier, self.last_flipped)
                self._flop_card_timeout = GLib.timeout_add(
                    FLOP_BACK_TIMEOUT,
                    self.flop_card, identifier, self.last_flipped)
            self.last_flipped = -1

    def flop_card(self, identifier, identifier2):
        self._flop_card_timeout = -1
        self._flop_cards = None

        self.emit('flop-card', identifier)
        self.model.grid[identifier]['state'] = '0'
        self.emit('flop-card', identifier2)
        self.model.grid[identifier2]['state'] = '0'

        # if self.model.data['divided'] == '1':
        #    self.card_highlighted(widget, -1, False)
        self.set_sensitive(True)
        self.flip_block = False
        self.change_turn()

    def card_highlighted(self, widget, identifier, mouse):
        self.emit('highlight-card', self.last_highlight, False)
        self.last_highlight = identifier

        if identifier == -1 or not self.sentitive:
            return

        if self.model.data['divided'] == '1':
            if self.last_flipped == -1 and identifier \
                    >= (len(self.model.grid) // 2):
                return
            if self.last_flipped != -1 and identifier \
                    < (len(self.model.grid) // 2):
                return

        if mouse and self.model.grid[identifier]['state'] == '0' or not mouse:
            self.emit('highlight-card', identifier, True)

    def increase_point(self, buddy, inc=1):
        self.players_score[buddy] += inc
        for i_ in range(inc):
            self.emit('increase-score', buddy)

    def get_grid(self):
        return self.model.grid

    def collect_data(self):
        for player, score in list(self.players_score.items()):
            index = self.players.index(player)
            score = self.players_score[player]
            self.model.data[str(index)] = str(score)
        return self.model.data

    def change_game(self, widget, game_name, size, mode,
                    title=None, color=None):
        if mode in ['file', 'demo']:
            logging.debug('change_game set is_demo mode %s', mode)
            self.model.is_demo = (mode == 'demo')
            if self.model.read(game_name) != 0:
                logging.error(' Reading setup file %s', game_name)
                return
        if mode == 'art4apps':
            # NOTE: i am using the same variables from the signal
            # to avoid addding more code
            category = game_name
            language = title
            color = None
            title = None
            self.model.is_demo = True
            self.model.read_art4apps(category, language)

        if size is None:
            size = int(self.model.data['size'])
        self.model.def_grid(size)

        if title is not None:
            self.model.data['title'] = title
        if color is not None:
            self.model.data['color'] = color
        self.load_remote(self.model.grid, self.model.data, mode, False)

    def reset_game(self, size=None):
        if size is None:
            size = int(self.model.data['size'])
        self.model.count = 0
        self.model.def_grid(size)
        self.load_remote(self.model.grid, self.model.data,
                         self.model.data['mode'], False)

    def set_load_mode(self, msg):
        self.emit('load_mode', msg)

    def set_sensitive(self, status):
        self.sentitive = status
        if not status:
            self.emit('highlight-card', self.last_highlight, False)

    def get_sensitive(self):
        return self.sentitive

    def get_current_player(self):
        return self.current_player

    def get_players_data(self):
        data = []
        for player, score in list(self.players_score.items()):
            data.append([player.props.key, player.props.nick,
                         player.props.color, score])
        return data

    def set_wait_list(self, wait_list):
        self.waiting_players = wait_list
        for w in wait_list:
            for p in self.players:
                if w[0] == p.props.key:
                    list.remove(w)
                    for i_ in range(w[3]):
                        self.increase_point(p)

    def set_myself(self, buddy):
        self.myself = buddy

    def add_to_waiting_list(self, buddy):
        self.players.remove(buddy)
        self.waiting_players.append(buddy)
        self.emit('wait_mode_buddy', buddy, True)

    def rem_to_waiting_list(self, buddy):
        self.waiting_players.remove(buddy)
        self.players.append(buddy)
        self.emit('wait_mode_buddy', buddy, False)

    def load_waiting_list(self, wait_list):
        for buddy in wait_list:
            self.add_to_waiting_list(buddy)

    def empty_waiting_list(self):
        for buddy in self.waiting_players:
            self.rem_to_waiting_list(buddy)
