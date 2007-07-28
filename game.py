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
import gtk

from sugar import profile
from dbus.service import method, signal
from dbus.gobject_service import ExportedGObject

import gobject

from model import Model

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
        self.model = Model(os.path.dirname(__file__))

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
        #gtk.gdk.threads_init()

            
    def load_game(self, game_name, size):        
        if self.model.read(game_name) == 0:
            self.model.def_grid(size)
            self.model.data['running'] = 'False'
            logging.debug(' Read setup file %s:   %s   '%(game_name, self.model.grid))
            self.emit('load_game', self.model.data, self.model.grid)
        else:
            logging.error(' Reading setup file %s'%game_name)
        
    def add_buddy(self, buddy, score = 0):
        _logger.debug('Buddy %r was added to game', buddy.props.nick)
        self.players.append(buddy)
        self.players_score[buddy] = score
        self.emit('add_buddy', buddy, score)
            
        if self.current_player == None:
            self.current_player = buddy
            self.change_turn()
    
    def rem_buddy(self, buddy):
        _logger.debug('Buddy %r was removed from game', buddy.props.nick)
        index = self.players.index(buddy)
        del self.players[index]
        del (self.players_score[buddy])
        if self.current_player == buddy and len(self.players) >= 2: ### fix from <> 0
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
        if self.model.data['divided'] == '1':
            if self.last_flipped == -1 and id >= (len(self.model.grid)/2):
                return
            if self.last_flipped <> -1 and id < (len(self.model.grid)/2):
                return
        self.model.data['running'] = 'True'

        # play sound in any case if available
        if self.sound == 1:
            snd = self.model.grid[id].get('snd', None)
            if snd != None:
                self.cs.perform('i 108 0.0 3.0 "%s" 1 0.9 0'%(os.path.join(os.path.dirname(__file__), snd)))                
                _logger.debug('Audio: play sound=%s'%snd)
                
        # First card case
        if self.last_flipped == -1:
            self.last_flipped = id
            self.model.grid[id]['state'] = '1'         
            self.emit('flip-card', id)
            if not signal:
                self.emit('flip-card-signal', id)    
                if self.model.data['divided'] == '1':
                    self.card_highlighted(widget, -1, False)

        # Pair matched        
        elif self.model.grid[self.last_flipped]['pairkey'] == self.model.grid[id]['pairkey']:
            stroke_color, fill_color = self.current_player.props.color.split(',')
            self.emit('set-border', id, stroke_color, fill_color)
            self.emit('set-border', self.last_flipped, stroke_color, fill_color)
            self.increase_point(self.current_player)
            self.model.grid[id]['state'] = '1'
            self.emit('flip-card', id)            
            if self.model.data['divided'] == '1':
                self.card_highlighted(widget, -1, False)
            if not signal:
                self.emit('flip-card-signal', id)
            self.last_flipped = -1
        # Pair don't match
        elif self.model.grid[self.last_flipped]['pairkey'] != self.model.grid[id]['pairkey']:
            self.emit('flip-card', id)
            if not signal:
                self.emit('flip-card-signal', id)
            self.model.grid[id]['state'] = '1'
            time.sleep(2) ### gobject.timeout() here?
            self.emit('flop-card', id)
            self.model.grid[id]['state'] = '0'
            self.emit('flop-card', self.last_flipped)
            if self.model.data['divided'] == '1':
                self.card_highlighted(widget, -1, False)
            # self.emit('highlight-card', id, True)
            self.model.grid[self.last_flipped]['state'] = '0'
            self.last_flipped = -1
            self.change_turn()
            
    def card_highlighted(self, widget, id, mouse):
        if id == -1:
            self.last_highlight = 1
            self.emit('highlight-card', self.last_highlight, False)
            return
        
        if not self.sentitive:
            return
        if self.model.data['divided'] == '1':
            if self.last_flipped == -1 and id >= (len(self.model.grid)/2):
                return
            if self.last_flipped <> -1 and id < (len(self.model.grid)/2):
                return
        self.emit('highlight-card', self.last_highlight, False)
        if mouse and self.model.grid[id]['state']=='0':            
            self.emit('highlight-card', id, True)
        if not mouse:
            self.emit('highlight-card', id, True)
        
        self.last_highlight = id
    
    def increase_point(self, buddy):
        self.players_score[buddy] += 1
        self.emit('increase-score', buddy)
        
    def get_grid(self):
        return self.model.grid

    def get_data(self):
        return self.model.data
    
    def change_game(self, game_name, size):
        if self.model.read(game_name) == 0:
            self.model.def_grid(size)
            self.load_remote(self.model.grid, self.model.data, False)                    
        else:
            logging.error(' Reading setup file %s'%game_name)        
        
    def load_remote(self, grid, data, signal = False):
        self.model.grid = grid
        self.model.data = data
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
        self.model.data['running'] = 'False'
        
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
