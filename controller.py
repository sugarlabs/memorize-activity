import logging

import gobject
import gtk
import os

from dbus import Interface
from dbus.service import method, signal
from dbus.gobject_service import ExportedGObject

from model import Model
from csound.csoundserver import CsoundServer

SERVICE = "org.freedesktop.Telepathy.Tube.Memosono"
IFACE = SERVICE
PATH = "/org/freedesktop/Telepathy/Tube/Memosono"


GAME_PATH = os.path.join(os.path.dirname(__file__),'games/drumgit')
IMAGES_PATH = os.path.join(os.path.dirname(__file__),'games/drumgit/images')
SOUNDS_PATH = os.path.join(os.path.dirname(__file__),'games/drumgit/sounds')
MAX_NUM_PLAYERS = 2

_logger = logging.getLogger('controller')


class Controller(ExportedGObject):
    ''' Networked Controller which is the core component of the activity. It
    handles the communication with the components (model, view) and with the
    other players over the network. 
    '''
    def __init__(self, tube, playview, is_initiator, buddies_panel, info_panel,
            owner, get_buddy, activity):
        super(Controller, self).__init__(tube, PATH)
        self.tube = tube
        self.pv = playview
        self.is_initiator = is_initiator
        self.entered = False
        self.buddies_panel = buddies_panel
        self.info_panel = info_panel
        self.owner = owner
        self._get_buddy = get_buddy
        self.activity = activity
        self.numplayers = 0
        self.turn = 0
        
        self.cs = CsoundServer()        
        gtk.gdk.threads_init()
        self.cs.start()
        
        if self.is_initiator:
            self.init_game()

        for tile in self.pv.tiles:
            tile.connect('button-press-event', self._button_press_cb, self.pv.tiles.index(tile))

            
        self.tube.watch_participants(self.participant_change_cb)


    def participant_change_cb(self, added, removed):

        _logger.debug('adding participants: %r', added)
        _logger.debug('removing participants: %r', removed)

        for handle, bus_name in added:
            buddy = self._get_buddy(handle)
            if buddy is not None:
                _logger.debug('buddy %r was added', buddy)
                if self.numplayers < MAX_NUM_PLAYERS:                    
                    self.buddies_panel.add_player(buddy)
                    self.numplayers+=1
                    if self.is_initiator:
                        self.buddies_panel.set_is_playing(buddy)
                        self.model.players[self.tube.participants[handle]] = [buddy.props.nick, 0]
                        _logger.debug('list of players: %s', self.model.players)                    
                else:
                    self.info_panel.show('we are already two players')
                    
        for handle in removed:
            buddy = self._get_buddy(handle)
            if buddy is not None:
                _logger.debug('buddy %r was removed', buddy)
                self.buddies_panel.remove_player(buddy)
                self.numplayers-=1
                if self.is_initiator:
                    try:
                        del self.model.players[self.tube.participants[handle]]
                    except ValueError:
                        # already absent
                        pass

        if not self.entered:
            self.playerid = self.tube.get_unique_name()
            self.tube.add_signal_receiver(self.info_cb, 'Info', IFACE,
                                          path=PATH, sender_keyword='sender')
            self.tube.add_signal_receiver(self.turn_cb, 'Turn', IFACE,
                                          path=PATH, sender_keyword='sender')
            self.tube.add_signal_receiver(self.flip_cb, 'Flip', IFACE,
                                          path=PATH, sender_keyword='sender')
            self.tube.add_signal_receiver(self.play_cb, 'Play', IFACE,
                                          path=PATH, sender_keyword='sender')
            self.tube.add_signal_receiver(self.points_cb, 'Points', IFACE,
                                          path=PATH, sender_keyword='sender')

            self.entered = True
            
        if self.is_initiator:        
            if len(self.model.players) == 2 and self.model.started == 0:
                _logger.debug('start the game')
                self.Info('start the game')
                self.model.started = 1
                self.change_turn()
            
    def init_game(self):
        _logger.debug('I am the initiator, so making myself the leader of the game.')
        self.model = Model(GAME_PATH, os.path.dirname(__file__))
        self.model.read('drumgit.mson')        
        self.model.def_grid()
        self.tube.add_signal_receiver(self.selected_cb, 'Selected', IFACE,
                                      path=PATH, sender_keyword='sender')

        
    @signal(dbus_interface=IFACE, signature='n')
    def Selected(self, tilenum):
        """Signal that a tile has been selected"""

    def selected_cb(self, tilenum, sender=None):
        _logger.debug('MA: %s flipped tile %d', sender, tilenum)        
        if self.model.grid[tilenum][2] == 1:
            self.Info('selected already')            
        else:
            pairkey, moch, state = self.model.grid[tilenum]
            color = self.model.pairs[pairkey].props.color

            if moch == 0:
                if self.model.pairs[pairkey].props.aimg != None:
                    img = os.path.join(IMAGES_PATH, self.model.pairs[pairkey].props.aimg)                
                    self.Flip(tilenum, img, color)
                if self.model.pairs[pairkey].props.asnd != None:
                    snd = os.path.join(SOUNDS_PATH, self.model.pairs[pairkey].props.asnd)
                    self.Play(tilenum, snd, color)
            elif moch == 1:
                if self.model.pairs[pairkey].props.bimg != None:
                    img = os.path.join(IMAGES_PATH, self.model.pairs[pairkey].props.bimg)
                    self.Flip(tilenum, img, color)
                if self.model.pairs[pairkey].props.bsnd != None:
                    snd = os.path.join(SOUNDS_PATH, self.model.pairs[pairkey].props.bsnd)
                    self.Play(tilenum, snd, color)
                        
            self.model.count+=1
            if self.model.count == 1:
                self.model.selected = tilenum
                self.model.grid[tilenum][2] = 1
                return 
            if self.model.count == 2:            
                self.model.count = 0
                # evaluate 
                if( self.model.same(tilenum, self.model.selected) == 1):                
                    _logger.debug('MA: Tile(%d) and (%d) are the same', tilenum, self.model.selected)
                    self.model.grid[tilenum][2] = 1
                    self.model.grid[self.model.selected][2] = 1
                
                    self.model.players[sender][1]+=1
                    self.Points(sender, self.model.players[sender][1])
                    self.Info('found pair, one more try')
                else:
                    self.model.grid[tilenum][2] = 0
                    self.model.grid[self.model.selected][2] = 0
                    self.change_turn()
                    self.Info('pair does not match, next player')
                    gobject.timeout_add(2000, self._turn_back, tilenum, self.model.selected)
                    _logger.debug('Tile(%d) and (%d) are NOT the same', tilenum, self.model.selected)

    def _turn_back(self, tilenuma, tilenumb):
        self.Flip(tilenuma, 'images/black.png', 100)
        self.Flip(tilenumb, 'images/black.png', 100)
        return False
    
    def change_turn(self):
        if self.model.player_active < (len(self.model.players)-1):
            self.model.player_active+=1
        else:
            self.model.player_active = 0

        key = self.model.players.keys()[self.model.player_active]
        self.Turn(key, self.model.players[key][0])
        
        
    @signal(dbus_interface=IFACE, signature='nsn')
    def Flip(self, tilenum, obj, color):
        """Signal that a tile will be flipped"""

    def flip_cb(self, tilenum, obj, color, sender=None):
        handle = self.tube.bus_name_to_handle[sender]
        _logger.debug('Flipped tile(%d) from %s. Show image.', tilenum, sender)
        self.pv.flip(tilenum, os.path.join(os.path.dirname(__file__), obj), color)            


    @signal(dbus_interface=IFACE, signature='nsn')
    def Play(self, tilenum, obj, color):
        """Signal that a sound will be played"""

    def play_cb(self, tilenum, obj, color, sender=None):
        handle = self.tube.bus_name_to_handle[sender]
        _logger.debug('Flipped tile(%d) from %s. Play sound.', tilenum, sender)        
        _logger.debug(' Sound: %s', obj)
        self.cs.perform('i 108 0.0 3.0 "%s" 1 0.7 0.5 0'%(obj))                


    @signal(dbus_interface=IFACE, signature='ss')
    def Turn(self, playerid, name):
        """Signal that it is the players turn"""

    def turn_cb(self, playerid, name, sender=None):
        if self.playerid == playerid:
            self.turn = 1
        else:
            self.turn = 0
            
        buddy = self._get_buddy(self.tube.bus_name_to_handle[playerid])
        self.buddies_panel.set_is_playing(buddy)
        self.info_panel.show('hey %s it is your turn'%name)

    @signal(dbus_interface=IFACE, signature='sn')
    def Points(self, player, points):
        """Signal to update the points"""

    def points_cb(self, player, points, sender=None):
        handle = self.tube.bus_name_to_handle[player]
        buddy = self._get_buddy(handle)
        self.buddies_panel.set_count(buddy, points)


    @signal(dbus_interface=IFACE, signature='s')
    def Info(self, msg):
        """Signal that there is some game information"""

    def info_cb(self, msg, sender=None):
        self.info_panel.show(msg)

            
    def _button_press_cb(self, tile, event, tilenum=None):
        if self.turn == 1:
            self.Selected(tilenum)
        else:
            _logger.debug('Not my turn')
            self.info_panel.show('Not my turn')        

        
