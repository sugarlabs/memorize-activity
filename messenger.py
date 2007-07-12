#! /usr/bin/env python
#
#    Copyright (C) 2007, One Laptop Per Child
#
#    Muriel de Souza Godoi - muriel@laptop.org
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
import dbus
from dbus.gobject_service import ExportedGObject

SERVICE = "org.laptop.Memorize"
IFACE = SERVICE
PATH = "/org/laptop/Memorize"

_logger = logging.getLogger('memorize-activity')

class Messenger(ExportedGObject):
    
    def __init__(self, tube, is_initiator, get_buddy, game):
        ExportedGObject.__init__(self, tube, PATH)
        self._tube = tube
        self.is_initiator = is_initiator
        self._get_buddy = get_buddy
        self.game = game
        self.ordered_bus_names = []
        self.entered = False        
        self._tube.watch_participants(self.participant_change_cb)

    def participant_change_cb(self, added, removed):
        if not self.entered:
            self._tube.add_signal_receiver(self._flip_receiver, '_flip_signal', IFACE, path=PATH, sender_keyword='sender')
            self._tube.add_signal_receiver(self._change_game_receiver, '_change_game_signal', IFACE, path=PATH, sender_keyword='sender')
            if self.is_initiator:
                _logger.debug('Initialising a new game, I am %s .', self._tube.get_unique_name())
                self.player_id = self._tube.get_unique_name()
                self.ordered_bus_names = [self.player_id]
                self._tube.add_signal_receiver(self._hello_receiver, '_hello_signal', IFACE, path=PATH, sender_keyword='sender')
            else:
                self._hello_signal()
        self.entered = True
        
    @dbus.service.signal(IFACE, signature='')
    def _hello_signal(self):
        ''' Notify current players that you joined '''
        _logger.debug('Sending hello to all')
    
    def _hello_receiver(self, sender=None):
        ''' Someone joined the game, so sync the new player '''
        _logger.debug('The new player %s has joined', sender)
        self.ordered_bus_names.append(sender)
        self._tube.get_object(sender, PATH).load_game(self.ordered_bus_names, self.game.get_grid(), self.game.get_data(), self.game.waiting_players, dbus_interface=IFACE)
    
    #@dbus.service.method(dbus_interface=IFACE, in_signature='asss', out_signature='')
    @dbus.service.method(dbus_interface=IFACE, in_signature='asa(ssssssssiii)a{ss}av', out_signature='')
    def load_game(self, bus_names, grid, data,list):
        ''' Sync the game with with players '''
        _logger.debug('Data received to sync game data')
        self.ordered_bus_names = bus_names
        self.player_id = bus_names.index(self._tube.get_unique_name())
        self._change_game_receiver(grid,data,self.ordered_bus_names[0])
        self.game.load_waiting_list(list)
        
    def flip(self, widget, id):
        ''' Notify other players that you flipped a card '''
        _logger.debug('Sending flip message: '+str(id))
        self._flip_signal(id)
    
    @dbus.service.signal(IFACE, signature='n')
    def _flip_signal(self, card_number):
        _logger.debug('Notifing other players that you flipped: %s', str(card_number))
        ''' Notify current players that you flipped a card '''

    def _flip_receiver(self, card_number, sender=None):
        ''' Someone flipped a card '''
        handle = self._tube.bus_name_to_handle[sender]
        
        if self._tube.self_handle <> handle:
            _logger.debug('Other player flipped: %s ', str(card_number))
            self.game.card_flipped(None, card_number, True)
       
    def change_game(self, sender, grid, data, waiting_list):
        ''' Notify other players that you changed the game '''
        _logger.debug('Sending changed game message')
        self._change_game_signal(grid, data)
    
    @dbus.service.signal(IFACE, signature='a(ssssssssiii)a{ss}')
    def _change_game_signal(self, grid, data):
        _logger.debug('Notifing other players that you changed the game')
        ''' Notify current players that you changed the game '''

    def _change_game_receiver(self, grid, data, sender=None):
        ''' Game changed by other player '''
        handle = self._tube.bus_name_to_handle[sender]
        
        if self._tube.self_handle <> handle:
            _logger.debug('Game changed by other player')
            new_grid = []
            for card in grid:
                new_grid.append(map(lambda x: str(x), card[:8])+[int(card[8]), int(card[9]), int(card[10])])
            self.game.load_remote(new_grid, data, True)
            