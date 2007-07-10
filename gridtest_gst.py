import gtk
import os
import random
import hippo
import gobject

import pygst
pygst.require("0.10")
import gst

from playview import PlayView
from gmodel import Model


GAME_PATH = os.path.join(os.path.dirname(__file__),'games/drumgit')
IMAGES_PATH = os.path.join(os.path.dirname(__file__),'games/drumgit/images')
SOUNDS_PATH = os.path.join(os.path.dirname(__file__),'games/drumgit/sounds')

class Test(object):
    def __init__(self):
        
        self.model = Model(GAME_PATH, os.path.dirname(__file__))
        self.model.read('drumgit.mson')        
        self.model.def_grid()
        print '%s' %self.model.pairs[0]._properties
        print '%s' %self.model.pairs[1]._properties
        print '%s' %self.model.pairs[2]._properties
        print 'self.grid: %s'%self.model.grid
    
        self.pv = PlayView( len(self.model.grid) )
        for tile in self.pv.tiles:
            tile.connect('button-press-event', self._button_press_cb, self.pv.tiles.index(tile))

        hbox = hippo.CanvasBox(spacing=4,
                               orientation=hippo.ORIENTATION_HORIZONTAL)
        hbox.append(self.pv, hippo.PACK_EXPAND)
        
        canvas = hippo.Canvas()
        canvas.set_root(hbox)

        window = gtk.Window()
        window.connect('destroy', gtk.main_quit)
        window.connect('key-press-event', self.key_press_cb)
        window.add(canvas)
        window.show_all()

        		
        self.player = gst.element_factory_make("playbin", "player")
        fakesink = gst.element_factory_make('fakesink', "my-fakesink")
        self.player.set_property("video-sink", fakesink)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)

        try:
            gtk.main()
        except KeyboardInterupt:
            pass
    
    def key_press_cb(self, window, event):
        if gtk.gdk.keyval_name(event.keyval) in ('Escape', 'q'):
            gtk.main_quit()

    def _button_press_cb(self, tile, event, tilenum=None):
        print 'selected tile=%s'%str(tilenum)
        pairkey, moch, state = self.model.grid[tilenum]
        color = self.model.pairs[pairkey].props.color
        if moch == 0:
            if self.model.pairs[pairkey].props.aimg != None:
                img = os.path.join(IMAGES_PATH, self.model.pairs[pairkey].props.aimg)                
                self.pv.flip(tilenum, img, color)
                gobject.timeout_add(2000, self._turn_back, tilenum) 
            if self.model.pairs[pairkey].props.asnd != None:
                snd = os.path.join(SOUNDS_PATH, self.model.pairs[pairkey].props.asnd)
                ssnd = os.path.join('/home/erikos/sugar-jhbuild/source/memosono', snd)
                print ssnd
                self.player.set_property('uri', "file://" + ssnd)
                self.player.set_state(gst.STATE_PLAYING)                 
        elif moch == 1:
            if self.model.pairs[pairkey].props.bimg != None:
                img = os.path.join(IMAGES_PATH, self.model.pairs[pairkey].props.bimg)
                self.pv.flip(tilenum, img, color)
                gobject.timeout_add(2000, self._turn_back, tilenum) 
            if self.model.pairs[pairkey].props.bsnd != None:
                snd = os.path.join(SOUNDS_PATH, self.model.pairs[pairkey].props.bsnd)
                ssnd = os.path.join('/home/erikos/sugar-jhbuild/source/memosono', snd)
                print ssnd
                self.player.set_property('uri', "file://" + ssnd)
                self.player.set_state(gst.STATE_PLAYING)

    def _turn_back(self, tilenum):
        self.pv.flip(tilenum, os.path.join(os.path.dirname(__file__), 'images/black.png'), 100)
        return False

    def on_message(self, bus, message):
        t = message.type
        print t
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)    
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)

if __name__ == '__main__':
    Test()
    gtk.gdk.threads_init()
