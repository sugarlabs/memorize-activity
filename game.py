#! /usr/bin/env python
#
#    Copyright (C) 2006, 2007, One Laptop Per Child
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

import os
import random
import logging
import gobject
import time

from sugar import profile
from dbus.service import method, signal
from dbus.gobject_service import ExportedGObject

import gobject

_logger = logging.getLogger('memorize-activity')

SERVICE = "org.laptop.Memorize"
IFACE = SERVICE
PATH = "/org/laptop/Memorize"


class MemorizeGame(gobject.GObject):
    
    __gsignals__ = {
        'reset_scoreboard': (gobject.SIGNAL_RUN_FIRST, None, []), 
        'reset_table': (gobject.SIGNAL_RUN_FIRST, None, []), 
        'load_game': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT]), 
        'change_game': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT]), 
        'change_game_signal': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT]), 
        'set-border': (gobject.SIGNAL_RUN_FIRST, None, [int, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT]), 
        'flip-card': (gobject.SIGNAL_RUN_FIRST, None, [int]), 
        'flip-card-signal': (gobject.SIGNAL_RUN_FIRST, None, [int]), 
        'flop-card': (gobject.SIGNAL_RUN_FIRST, None, [int]), 
        'highlight-card': (gobject.SIGNAL_RUN_FIRST, None, [int, gobject.TYPE_PYOBJECT]), 
        'add_buddy': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT, int]), 
        'rem_buddy': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT]), 
        'increase-score': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT]), 
        'wait_mode_buddy': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT]),
        'change-turn': (gobject.SIGNAL_RUN_FIRST, None, [gobject.TYPE_PYOBJECT]), 
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
        self.game_dir = os.path.join(os.path.dirname(__file__), 'games')
        self.messenger = None
        self.sentitive = True
        
    def load_game(self, game_name, size):
        tuple = self.read_config(game_name, size)
        self.data = tuple[0]
        self.grid = tuple[1]
        self.data['running'] = 'False'
        self.emit('load_game', self.data, self.grid)
        
    def add_buddy(self, buddy, score = 0):
        _logger.debug('Buddy %r was added to game', buddy.props.nick)
        self.players.append(buddy)
        self.players_score[buddy] = score
        self.emit('add_buddy', buddy, score)
            
        if self.current_player == None:
            self.current_player = buddy
            self.change_turn()
    
    def rem_buddy(self, buddy):
        _logger.debug('Buddy %r was removed to game', buddy.props.nick)
        index = self.players.index(buddy)
        del self.players[index]
        del (self.players_score[buddy])
        if self.current_player == buddy and len(self.players) <> 0:
            self.change_turn()
        self.emit('rem_buddy', buddy)

    def change_turn(self):
        if self.current_player == None:
            self.current_player = self.players[0]
        elif self.current_player == self.players[-1]:
            self.current_player = self.players[0]
        else:
            self.current_player = self.players[self.players.index(self.current_player)+1]
        self.set_sensitive(self.current_player == self.myself)
        self.emit('change-turn', self.current_player)   
                        
    def card_flipped(self, widget, id, signal = False):
        # Check if is my turn
        if not self.sentitive and not signal:
            return
        
        # Handle groups if needed
        if self.data['divided'] == 'True':
            if self.last_flipped == -1 and id >= (len(self.grid)/2):
                return
            if self.last_flipped <> -1 and id < (len(self.grid)/2):
                return
        self.data['running'] = 'True'
            
        # First card case
        if self.last_flipped == -1:
            self.last_flipped = id
            self.grid[id][8] = 1
            self.emit('flip-card', id)
            if not signal:
                self.emit('flip-card-signal', id)    
                if self.data['divided'] == 'True':
                    self.card_highlighted(widget, -1, False)

        # Pair matched
        elif self.grid[self.last_flipped][-1] == self.grid[id][-1]:
            stroke_color, fill_color = self.current_player.props.color.split(',')
            self.emit('set-border', id, stroke_color, fill_color)
            self.emit('set-border', self.last_flipped, stroke_color, fill_color)
            self.increase_point(self.current_player)
            self.grid[id][8] = 1
            self.emit('flip-card', id)
            if self.data['divided'] == 'True':
                self.card_highlighted(widget, -1, False)
            if not signal:
                self.emit('flip-card-signal', id)
            self.last_flipped = -1
        # Pair don't match
        elif self.grid[self.last_flipped][-1] <> self.grid[id][-1]:
            self.emit('flip-card', id)
            if not signal:
                self.emit('flip-card-signal', id)
            self.grid[id][8] = 1
            time.sleep(2)
            self.emit('flop-card', id)
            self.grid[id][8] = 0
            self.emit('flop-card', self.last_flipped)
            if self.data['divided'] == 'True':
                self.card_highlighted(widget, -1, False)
            # self.emit('highlight-card', id, True)
            self.grid[self.last_flipped][8] = 0
            self.last_flipped = -1
            self.change_turn()
            
    def card_highlighted(self, widget, id, mouse):
        if id == -1:
            self.last_highlight = 1
            self.emit('highlight-card', self.last_highlight, False)
            return
        
        if not self.sentitive:
            return
        if self.data['divided'] == 'True':
            if self.last_flipped == -1 and id >= (len(self.grid)/2):
                return
            if self.last_flipped <> -1 and id < (len(self.grid)/2):
                return
        self.emit('highlight-card', self.last_highlight, False)
        if mouse and self.grid[id][8]==0:            
            self.emit('highlight-card', id, True)
        if not mouse:
            self.emit('highlight-card', id, True)
        
        self.last_highlight = id
    
    def increase_point(self, buddy):
        self.players_score[buddy] += 1
        self.emit('increase-score', buddy)
                
    def read_config(self, game_name, size = 100):
        filename = os.path.join(self.game_dir, game_name +'/'+game_name+'.mem')
        # seed = random.randint(0, 14567)
        temp1 = []
        temp2 = []
        grid = []
        data = {}
        # set random seed
        random.seed()
        filecheck = filename.split('.')
        if filecheck[2] != 'mem':
            logging.error('File format of %s'%filename)
        else:    
            fd = open(filename, 'r')
            if fd == None:
                logging.error(' Reading setup file %s'%filename)
            else:# set random seed
                logging.info(' Read setup for memosono from file %s'%filename)        
                lines = fd.readlines()
                index = 0
                
                # Load variables
                while lines[index][0] != '#':
                    zw = lines[index].split('=')
                    zw[1] = zw[1][:-1]
                    if len(zw) is not 0:
                        data[zw[0]]=zw[1]
                        index += 1
                index += 1
                data['size'] = str(size)
                
                # Load cards data
                tile_number = 0
                card_num = len(lines)-index
                while tile_number < card_num  and tile_number <= int((size*size)/2)-1:
                    zw = lines[index].split(',')
                    if len(zw) is not 0:
                        temp1.append(zw[:8]+[ 0, 0, tile_number])
                        temp2.append(zw[8:]+[ 0, 0, tile_number])
                        tile_number += 1
                    index += 1
                fd.close()
                
                # Shuffle cards order
                if data['divided']=='True':                
                    random.shuffle(temp1)
                    random.shuffle(temp2)
                    temp1.extend(temp2)
                else:
                    temp1.extend(temp2)
                    random.shuffle(temp1)

            return data, temp1
        
    def get_grid(self):
        return self.grid

    def get_data(self):
        return self.data
    
    def change_game(self, game_name, size):
        tuple = self.read_config(game_name, size)
        data = tuple[0]
        grid = tuple[1]
        self.load_remote(grid, data, False)
        
        
    def load_remote(self, grid, data, signal = False):
        self.grid = grid
        self.data = data
        self.emit('reset_scoreboard')
        self.emit('change_game', self.get_data(), self.get_grid())
        if not signal:
            self.emit('change_game_signal', self.get_grid(), self.get_data(), self.waiting_players)
        for buddy in self.players:
            self.players_score[buddy] = 0
        self.current_player = None
        self.last_flipped = -1
        self.last_highlight = 1
        self.change_turn()
        self.data['running'] = 'False'
        
    def set_messenger(self, messenger):
        self.messenger = messenger
 
    def set_sensitive(self, status):
        self.sentitive = status
        if not status:
            self.emit('highlight-card', self.last_highlight, False)
        else:
            self.emit('highlight-card', self.last_highlight, True)
    def get_sensitive(self):
        return self.sentitive
    
    def get_current_player(self):
        return self.current_player
    
    def set_myself(self, buddy):
        self.myself = buddy
        
    def add_to_waiting_list(self,buddy):
        self.players.remove(buddy)
        self.waiting_players.append(buddy)
        self.emit('wait_mode_buddy',buddy,True)
    
    def rem_to_waiting_list(self,buddy):
        self.waiting_players.remove(buddy)
        self.players.append(buddy)
        self.emit('wait_mode_buddy',buddy,False)
        
    def load_waiting_list(self,list):
        for buddy in list:
            self.add_to_waiting_list(buddy)
            
    def empty_waiting_list(self):
        for buddy in self.waiting_players:
            self.rem_to_waiting_list(buddy)
