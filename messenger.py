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
_logger = logging.getLogger('memorize-activity')

import tempfile
from os import environ, chmod
from os.path import join, getsize, isfile, dirname, basename
from dbus.service import method, signal
from dbus.gobject_service import ExportedGObject
from sugar.datastore import datastore
from gettext import gettext as _

SERVICE = 'org.laptop.Memorize'
IFACE = SERVICE
PATH = '/org/laptop/Memorize'

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
        self.files = {}

    def participant_change_cb(self, added, removed):
        if not self.entered:
            self._flip_handler()
            self._change_game_handler()
            self._file_part_handler()
            if self.is_initiator:
                self.player_id = self._tube.get_unique_name()
                self.ordered_bus_names = [self.player_id]
                self._hello_handler()
            else:
                self._hello_signal()
        self.entered = True
    
    # hello methods    
   
    @signal(IFACE, signature='')
    def _hello_signal(self):
        pass
    
    def _hello_handler(self):
        self._tube.add_signal_receiver(self._hello_receiver, 
                                       '_hello_signal', 
                                       IFACE, 
                                       path=PATH, 
                                       sender_keyword='sender')
    
    def _hello_receiver(self, sender=None):
        self.ordered_bus_names.append(sender)
        data = self.game.model.data
        path = data['game_file']
        if self.game.model.data['mode'] == 'file':
             title = data.get('title', 'Received game')
             color = data.get('color', '#ff00ff,#00ff00')
             self.file_sender(sender, path, title, color)
        
        remote_object = self._tube.get_object(sender, PATH)
        remote_object.load_game(self.ordered_bus_names, 
                                self.game.get_grid(), 
                                self.game.get_data(), 
                                self.game.players.index(self.game.current_player), 
                                #self.game.waiting_players,
                                path)
    
    @method(dbus_interface=IFACE, in_signature='asaa{ss}a{ss}ns', out_signature='', byte_arrays=True)
    def load_game(self, bus_names, grid, data, current_player, path):
        self.ordered_bus_names = bus_names
        self.player_id = bus_names.index(self._tube.get_unique_name())
        #self.game.load_waiting_list(list)
        self.game.current_player = self.game.players[current_player]
        self._change_game_receiver(data['mode'], grid, data, path)
    
    # Change game method
    
    def change_game(self, sender, mode, grid, data, waiting_list, zip):
        path = self.game.model.data['game_file']
        
        if mode == 'file':
            title = data.get('title', 'Received game')
            color = data.get('color', '')    
            self.file_sender('all', path, title, color)    

        self._change_game_signal(mode, grid, data, path)
    
    def _change_game_handler(self):
        self._tube.add_signal_receiver(self._change_game_receiver, 
                                       '_change_game_signal', 
                                        IFACE, path=PATH, 
                                        sender_keyword='sender', 
                                        byte_arrays=True)
    
    @signal(IFACE, signature='saa{ss}a{ss}s')
    def _change_game_signal(self, mode, grid, data, path):
        pass
    
    def _change_game_receiver(self, mode, grid, data, path, sender=None):
        # ignore my own signal
        if sender == self._tube.get_unique_name():
            return
        if mode == 'demo':
            game_name = basename(data.get('game_file', 'debug-demo'))
            game_file = join(dirname(__file__), 'demos', game_name).encode('ascii')
            self.game.model.read(game_file)
        if mode == 'file':
            self.game.model.read(self.files[path])
        
        if self.game.model.data.has_key('path'):    
            data['path'] = self.game.model.data['path']
            data['pathimg'] = self.game.model.data['pathimg']
            data['pathsnd'] = self.game.model.data['pathsnd']
        self.game.load_remote(grid, data, mode, True)
               
    # File transfer methods

    def file_sender(self, target, filename, title, color):
        size = getsize(filename)
        f = open(filename, 'rb')
        part_size = 8192
        num_parts = (size / part_size) +1
        for part in range(num_parts):
            bytes = f.read(part_size)
            self._file_part_signal(target, filename, part+1, num_parts, bytes, title, color)
        f.close()
    
    @signal(dbus_interface=IFACE, signature='ssuuayss')
    def _file_part_signal(self, target, filename, part, numparts, bytes, title, color):
        pass
        
    def _file_part_handler(self):
        self._tube.add_signal_receiver(self._file_part_receiver, 
                                        '_file_part_signal', 
                                        IFACE, 
                                        path=PATH, 
                                        sender_keyword='sender', 
                                        byte_arrays=True)
        
    def _file_part_receiver(self, target, filename, part, numparts, bytes, title=None, color=None, sender=None):
        # ignore my own signal
        if sender == self._tube.get_unique_name():
            return
        
        if not (target == 'all' or target == self._tube.get_unique_name()):
            return
        
        # first chunk
        if part == 1:
            tmp_root = join(environ['SUGAR_ACTIVITY_ROOT'], 'instance')
            temp_dir = tempfile.mkdtemp(dir=tmp_root)
            chmod(temp_dir,0777)
            self.temp_file = join(temp_dir, 'game.zip')
            self.files[filename] = self.temp_file
            self.f = open(self.temp_file, 'a+b')
        
        self.f.write(bytes)
        
        percentage = int(float(part) / float(numparts) * 100.0)
        self.game.set_load_mode(_('Receiving game') + ': ' + str(percentage) + '% ' + _('done') + '.')
            
        # last chunk
        if part == numparts:
            self.f.close()   
            #file = self.files[filename]
            # Saves the zip in datastore
            gameObject = datastore.create()
            gameObject.metadata['title'] = title
            gameObject.metadata['mime_type'] = 'application/x-memorize-project'
            gameObject.metadata['icon-color'] = color
            gameObject.file_path = self.temp_file
            datastore.write(gameObject)
            #gameObject.destroy()
             

    # flip card methods         

    def flip_sender(self, widget, id):
        self._flip_signal(id)
    
    def _flip_handler(self):
        self._tube.add_signal_receiver(self._flip_receiver, 
                                       '_flip_signal', 
                                       IFACE, 
                                       path=PATH, 
                                       sender_keyword='sender')
    
    @signal(IFACE, signature='n')
    def _flip_signal(self, card_number):
        pass

    def _flip_receiver(self, card_number, sender=None):
        # ignore my own signal
        if sender == self._tube.get_unique_name():
            return
        self.game.card_flipped(None, card_number, True)
            
