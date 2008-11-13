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

import logging
import gobject
from os.path import join, dirname

from gettext import gettext as _
from sugar import profile
from dbus.service import method, signal
from dbus.gobject_service import ExportedGObject
from gobject import SIGNAL_RUN_FIRST, TYPE_PYOBJECT, GObject, timeout_add

from model import Model

_logger = logging.getLogger('memorize-activity')

SERVICE = 'org.laptop.Memorize'
IFACE = SERVICE
PATH = '/org/laptop/Memorize'


class MemorizeGame(GObject):
    
    __gsignals__ = {
        'reset_scoreboard': (SIGNAL_RUN_FIRST, None, []), 
        'reset_table': (SIGNAL_RUN_FIRST, None, []), 
        'load_mode': (SIGNAL_RUN_FIRST, None, [TYPE_PYOBJECT]), 
        'load_game': (SIGNAL_RUN_FIRST, None, 2 * [TYPE_PYOBJECT]), 
        'change_game': (SIGNAL_RUN_FIRST, None, 2 * [TYPE_PYOBJECT]), 
        'change_game_signal': (SIGNAL_RUN_FIRST, None, 5 * [TYPE_PYOBJECT]), 
        'set-border': (SIGNAL_RUN_FIRST, None, 3 * [TYPE_PYOBJECT]), 
        'flip-card': (SIGNAL_RUN_FIRST, None, [int]), 
        'flip-card-signal': (SIGNAL_RUN_FIRST, None, [int]), 
        'flop-card': (SIGNAL_RUN_FIRST, None, [int]), 
        'highlight-card': (SIGNAL_RUN_FIRST, None, 2 * [TYPE_PYOBJECT]), 
        'add_buddy': (SIGNAL_RUN_FIRST, None, 2 * [TYPE_PYOBJECT]), 
        'rem_buddy': (SIGNAL_RUN_FIRST, None, [TYPE_PYOBJECT]), 
        'increase-score': (SIGNAL_RUN_FIRST, None, [TYPE_PYOBJECT]), 
        'wait_mode_buddy': (SIGNAL_RUN_FIRST, None, 2 * [TYPE_PYOBJECT]), 
        'msg_buddy': (SIGNAL_RUN_FIRST, None, 2 * [TYPE_PYOBJECT]), 
        'change-turn': (SIGNAL_RUN_FIRST, None, [TYPE_PYOBJECT]), 
        }
    
    def __init__(self):
        gobject.GObject.__init__(self)
        self.myself = None
        self.players_score = {}
        self.players = []
        self.waiting_players = []
        self.current_player = None
        self.last_flipped = -1
        self.last_highlight = 1
        self.game_dir = join(dirname(__file__), 'games')
        self.messenger = None
        self.sentitive = True
        self.model = Model(dirname(__file__))
        self.flip_block = False

        # create csound instance to play sound files
        self.sound = 0        
        try:
            import csnd
            del csnd
            self.sound = 1
            _logger.error(' [Check for module csnd] found.')
        except:
            _logger.error(' [Check for module csnd] not found. There will be no sound.')

        if self.sound == 1:
            from csound.csoundserver import CsoundServer            
            self.cs = CsoundServer()        
            if self.cs.start() != 0:
                _logger.error(' Error starting csound performance.')
                self.sound = 0
            
    def load_game(self, game_name, size, mode):
        self.set_load_mode('Loading game')   
        if self.model.read(game_name) == 0:
            self.model.def_grid(size)
            self.model.data['running'] = 'False'
            self.model.data['mode'] = mode
            logging.debug(' Read setup file %s: %s '%(game_name, self.model.grid))
            self.emit('load_game', self.model.data, self.model.grid)
        else:
            logging.error(' Reading setup file %s'%game_name)
    
    def load_remote(self, grid, data, mode, signal = False):
        self.set_load_mode(_('Loading game...'))
        self.model.grid = grid
        self.model.data = data
        self.model.data['mode'] = mode
        self.emit('reset_scoreboard')
        if not signal:
            self.emit('change_game_signal', 
                      mode, 
                      self.get_grid(), 
                      self.get_data(), 
                      self.waiting_players, 
                      self.model.data['game_file'])
        self.emit('change_game', self.get_data(), self.get_grid())
        for buddy in self.players:
            self.players_score[buddy] = 0
        self.current_player = None
        self.last_flipped = -1
        self.last_highlight = 1
        self.change_turn()
        self.model.data['running'] = 'False'
        
        for card in self.model.grid:
            if card['state'] == '1':           
                self.emit('flip-card', self.model.grid.index(card))
                self.last_flipped = self.model.grid.index(card)
            elif card['state'] != '0':  
                stroke_color, fill_color = card['state'].split(',')
                self.emit('flip-card', self.model.grid.index(card))
                self.emit('set-border', self.model.grid.index(card), stroke_color, fill_color)
        
    def add_buddy(self, buddy, score = 0):
        _logger.debug('Buddy %r was added to game', buddy.props.nick)
        self.players.append(buddy)
        self.players_score[buddy] = score
        self.emit('add_buddy', buddy, score)
        logging.debug(str(buddy))
            
        if self.current_player == None:
            self.current_player = buddy
            self.change_turn()
    
    def rem_buddy(self, buddy):
        _logger.debug('Buddy %r was removed from game', buddy.props.nick)
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

    def change_turn(self):
        if len(self.players) <= 1:
            self.current_player = self.players[0]
        if self.current_player == None:
            self.current_player = self.players[0]
        elif self.current_player == self.players[-1]:
            self.current_player = self.players[0]
        else:
            next = self.players[self.players.index(self.current_player)+1]
            self.current_player = next
        self.set_sensitive(self.current_player == self.myself)
        self.emit('change-turn', self.current_player)   
                        
    def play_sound(self, snd, sound_file):
        if len(snd.split('.')) > 1:
            if snd.split('.')[1] in ['wav', 'aif', 'aiff']:
                self.cs.perform('i 102 0.0 3.0 "%s" 1 0.9 0'%(sound_file))                
            else:
                self.cs.perform('i 100 0.0 3.0 "%s" 1 0.9 0'%(sound_file))                
    
    def card_flipped(self, widget, id, signal = False):        
                
        # Check if is my turn
        if (not self.sentitive and not signal) or self.last_flipped == id:
            return
        
        # Handle groups if needed
        if self.model.data.get('divided') == '1':
            if self.last_flipped == -1 and id >= (len(self.model.grid)/2):
                return
            if self.last_flipped <> -1 and id < (len(self.model.grid)/2):
                return
            
        # do not process flips when flipping back
        if self.flip_block:
            return
        else:
            self.flip_block = True
            
        self.model.data['running'] = 'True'

        # play sound in case if available
        if self.sound == 1:
            snd = self.model.grid[id].get('snd', None)
            if snd != None:
                sound_file = join(self.model.data.get('pathsnd'), snd)
                self.play_sound(snd, sound_file)
                
        self.emit('flip-card', id)
        if not signal:
            self.emit('flip-card-signal', id)
        
        # First card case
        if self.last_flipped == -1:
            self.last_flipped = id
            self.model.grid[id]['state'] = '1'         
            self.flip_block = False

        # Second card case
        else:
            # Pair matched
            pair_key_1 = self.model.grid[self.last_flipped]['pairkey']
            pair_key_2 = self.model.grid[id]['pairkey']
            
            if pair_key_1 == pair_key_2:
                stroke_color, fill_color = self.current_player.props.color.split(',')
                self.emit('set-border', id, stroke_color, fill_color)
                self.emit('set-border', self.last_flipped, stroke_color, fill_color)
                
                self.increase_point(self.current_player)
                self.model.grid[id]['state'] = self.current_player.props.color
                self.model.grid[self.last_flipped]['state'] = self.current_player.props.color
                self.flip_block = False        
            # Pair didn't match
            else:
                self.model.grid[id]['state'] = '1'
                self.set_sensitive(False)
                timeout_add(2000, self.flop_card, id, self.last_flipped)
            self.last_flipped = -1
                
    def flop_card(self, id, id2):
        self.emit('flop-card', id)
        self.model.grid[id]['state'] = '0'
        self.emit('flop-card', id2)
        self.model.grid[id2]['state'] = '0'
        
        #if self.model.data['divided'] == '1':
        #    self.card_highlighted(widget, -1, False)
        self.set_sensitive(True)
        self.flip_block = False
        self.change_turn()

    def card_highlighted(self, widget, id, mouse):
        self.emit('highlight-card', self.last_highlight, False)
        self.last_highlight = id
       
        if id == -1 or not self.sentitive:
            return

        if self.model.data['divided'] == '1':
            if self.last_flipped == -1 and id >= (len(self.model.grid)/2):
                return
            if self.last_flipped <> -1 and id < (len(self.model.grid)/2):
                return

        if mouse and self.model.grid[id]['state']=='0' or not mouse:            
            self.emit('highlight-card', id, True)

    
    def increase_point(self, buddy):
        self.players_score[buddy] += 1
        self.emit('increase-score', buddy)
        
    def get_grid(self):
        return self.model.grid

    def get_data(self):
        return self.model.data
    
    def change_game(self, widget, game_name, size, mode, title = None, color= None):
        if mode in ['file', 'demo']:
            if self.model.read(game_name) != 0:
                logging.error(' Reading setup file %s'%game_name)
                return
        if size == None:
            size = int(self.model.data['size'])
        self.model.def_grid(size)
        
        if title != None:
            self.model.data['title'] = title
        if color != None:
            self.model.data['color'] = color
        self.load_remote(self.model.grid, self.model.data, mode, False)                    
            
    def reset_game(self, size = None):
        if size == None:
            size = int(self.model.data['size'])
        self.model.def_grid(size)    
        self.load_remote(self.model.grid, self.model.data, False) 
        
    def set_load_mode(self, msg):
        self.emit('load_mode', msg)      
    
    def set_messenger(self, messenger):
        self.messenger = messenger
 
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
        for player, score  in self.players_score.items():
            data.append([player.props.key, player.props.nick, player.props.color, score])
        return data
    
    def set_wait_list(self, list):
        self.waiting_players = list
        for w in list:
            for p in self.players:
                if  w[0] == p.props.key:
                    list.remove(w)
                    for i in range(w[3]):
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
        
    def load_waiting_list(self, list):
        for buddy in list:
            self.add_to_waiting_list(buddy)
            
    def empty_waiting_list(self):
        for buddy in self.waiting_players:
            self.rem_to_waiting_list(buddy)
