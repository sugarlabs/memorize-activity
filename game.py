import logging

import gtk
import os

from dbus import Interface
from dbus.service import method, signal
from dbus.gobject_service import ExportedGObject


# XXX: I'm not convinced this is in the right namespace
SERVICE = "org.freedesktop.Telepathy.Tube.Memosono"
IFACE = SERVICE
PATH = "/org/freedesktop/Telepathy/Tube/Memosono"


_logger = logging.getLogger('memosono-activity.game')


class ConnectGame(ExportedGObject):

    def __init__(self, tube, playview, model, is_initiator, buddies_panel, info_panel,
            owner, get_buddy, activity):
        super(ConnectGame, self).__init__(tube, PATH)
        self.tube = tube
        self.pv = playview
        self.model = model
        self.is_initiator = is_initiator
        self.entered = False
        self.player_id = None
        self.buddies_panel = buddies_panel
        self.info_panel = info_panel
        self.owner = owner
        self._get_buddy = get_buddy
        self.activity = activity

        self.active_player = 1
        self.count = 0
        self.points = {}
        
        # list indexed by player ID
        # 0, 1 are players 0, 1
        # 2+ are the spectator queue, 2 is to play next
        self.ordered_bus_names = []

        for tile in self.pv.tiles:
            tile.connect('button-press-event', self._button_press_cb, self.pv.tiles.index(tile))

        self.tube.watch_participants(self.participant_change_cb)

    def participant_change_cb(self, added, removed):
        # Initiator is player 0, other player is player 1.

        _logger.debug('adding participants: %r', added)
        _logger.debug('removing participants: %r', removed)

        for handle, bus_name in added:
            buddy = self._get_buddy(handle)
            _logger.debug('Buddy %r was added', buddy)
            if buddy is not None:
                self.buddies_panel.add_watcher(buddy)

        for handle in removed:
            buddy = self._get_buddy(handle)
            _logger.debug('Buddy %r was removed', buddy)
            if buddy is not None:
                self.buddies_panel.remove_watcher(buddy)
            try:
                self.ordered_bus_names.remove(self.tube.participants[handle])
            except ValueError:
                # already absent
                pass

        if not self.entered:
            self.tube.add_signal_receiver(self.flip_cb, 'Flip', IFACE,
                path=PATH, sender_keyword='sender')
            if self.is_initiator:
                _logger.debug('I am the initiator, so making myself player 0')
                self.add_hello_handler()
                self.ordered_bus_names = [self.tube.get_unique_name()]
                self.player_id = 0
                self.points[self.player_id] = 0
                self.buddies_panel.add_player(self.owner)
            else:
                _logger.debug('Hello, everyone! What did I miss?')
                self.Hello()
        self.entered = True

    @signal(dbus_interface=IFACE, signature='')
    def Hello(self):
        """Request that this player's Welcome method is called to bring it
        up to date with the game state.
        """

    @method(dbus_interface=IFACE, in_signature='aanas', out_signature='')
    def Welcome(self, grid, bus_names):
        """To be called on the incoming player by the other players to
        inform them of the game state.

        FIXME: nominate a "referee" (initially the initiator) responsible
        for saying Welcome, elect a new referee when the current referee
        leaves? This could also be used to make the protocol robust against
        cheating/bugs
        """
        if self.player_id is None:
            _logger.debug('Welcomed to the game. Player bus names are %r',
                          bus_names)
            _logger.debug('Received the grid:  %s', str(grid))
            self.model.grid = grid

            self.ordered_bus_names = bus_names
            self.player_id = bus_names.index(self.tube.get_unique_name())
            self.points[self.player_id] = 0
            # OK, now I'm synched with the game, I can welcome others
            self.add_hello_handler()

            buddy = self._get_buddy(self.tube.bus_name_to_handle[bus_names[0]])
            self.buddies_panel.add_player(buddy)
            buddy = self._get_buddy(self.tube.bus_name_to_handle[bus_names[1]])
            self.buddies_panel.add_player(buddy)

            if self.active_player == self.player_id:
                _logger.debug("It's my turn already!")
                self.change_turn()
        else:
            _logger.debug("I've already been welcomed, doing nothing")

    def add_hello_handler(self):
        self.tube.add_signal_receiver(self.hello_cb, 'Hello', IFACE,
            path=PATH, sender_keyword='sender')

    @signal(dbus_interface=IFACE, signature='nsn')
    def Flip(self, tilenum, obj, color):
        """Signal that the local player has flipped a tile."""

    def hello_cb(self, sender=None):
        """Tell the newcomer what's going on."""
        _logger.debug('Newcomer %s has joined', sender)
        self.ordered_bus_names.append(sender)
        if len(self.ordered_bus_names) == 2:
            buddy = self._get_buddy(self.tube.bus_name_to_handle[sender])
            self.buddies_panel.add_player(buddy)
        _logger.debug('Bus names are now: %r', self.ordered_bus_names)
        _logger.debug('Welcoming newcomer and sending them the game state')
        grid = 0
        self.tube.get_object(sender, PATH).Welcome(self.model.grid,
                                                   self.ordered_bus_names,
                                                   dbus_interface=IFACE)
        _logger.debug('--- After welcome')
        if (self.player_id == 0 and len(self.ordered_bus_names) == 2):
            _logger.debug("This is my game and an opponent has joined. "
                          "I go first")
            self.change_turn()

    def flip_cb(self, tilenum, obj, color, sender=None):
        handle = self.tube.bus_name_to_handle[sender]
        _logger.debug('Flipped tile(%d) from %s', tilenum, sender)

        self.pv.flip(tilenum, obj, color)            

        self.count+=1
        if self.count == 1:
            self.comp = tilenum
        if self.count == 2:            
            self.count = 0
            # evaluate 
            if( self.model.same(tilenum, self.comp) == 1):                
                _logger.debug('Tile(%d) and (%d) are the same', tilenum, self.comp)
                buddy = self._get_buddy(handle)
                self.points[self.active_player]+=1
                self.buddies_panel.set_count(buddy, self.points[self.active_player])
                self.info_panel.show('Open another one')
            else:
                _logger.debug('Tile(%d) and (%d) are NOT the same', tilenum, self.comp)
                # next player
                self.change_turn()

    def change_turn(self):
        self.set_active_player()
        try:
            bus_name = self.ordered_bus_names[self.active_player]
            buddy = self._get_buddy(self.tube.bus_name_to_handle[bus_name])
            self.buddies_panel.set_is_playing(buddy)
        except:
            _logger.error('argh!', exc_info=1)
            raise

        if self.active_player == self.player_id:
            _logger.debug('It\'s my turn now')
            self.info_panel.show('Your turn')
            self.activity.grab_focus()
        else:
            _logger.debug('It\'s not my turn')
            self.info_panel.show('Other player\'s turn')
            

    def set_active_player(self):
        if self.active_player == 0:
            self.active_player = 1
        else:
            self.active_player = 0

    def _button_press_cb(self, tile, event, tilenum=None):
        if self.active_player != self.player_id:
            _logger.debug('Ignoring flip - not my turn')
        else:        
            _logger.debug('selected tile=%s'%str(tilenum))
            obj, color = self.model.gettile(tilenum)
            self.Flip(tilenum, obj, color)
        
