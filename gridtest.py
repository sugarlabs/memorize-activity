import gtk
import os
import random
import hippo
import gobject

from playview import PlayView
from model import Model

GAME_PATH = os.path.join(os.path.dirname(__file__),'games/drumgit')
IMAGES_PATH = os.path.join(os.path.dirname(__file__),'games/drumgit/images')

class Test(object):
    def __init__(self):
        
        self.model = Model(GAME_PATH, os.path.dirname(__file__))
        self.model.read('drumgit.mson')        
        print 'pairs: %s' %self.model.pairs

        ### create grid from pairs information
        self.grid = []                
        for key in self.model.pairs.iterkeys():
            self.grid.append((key, 0))
            self.grid.append((key, 1))
        print 'self.grid: %s'%self.grid

        ### shuffle the grid tiles
        random.shuffle(self.grid)
        print 'self.grid after shufle: %s'%self.grid
        
        self.pv = PlayView( len(self.grid) )
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
        try:
            gtk.main()
        except KeyboardInterupt:
            pass
        
    def key_press_cb(self, window, event):
        if gtk.gdk.keyval_name(event.keyval) in ('Escape', 'q'):
            gtk.main_quit()

    def _button_press_cb(self, tile, event, tilenum=None):
        print 'selected tile=%s'%str(tilenum)
        pairkey, moch = self.grid[tilenum]
        obj = os.path.join(IMAGES_PATH, self.model.pairs[pairkey][moch])
        color = self.model.pairs[pairkey][2]
        print 'obj=%s color=%s'%(obj, color)
        self.pv.flip(tilenum, obj, color)
        gobject.timeout_add(2000, self._turn_back, tilenum) 

    def _turn_back(self, tilenum):
        self.pv.flip(tilenum, os.path.join(os.path.dirname(__file__), 'images/black.png'), 100)
        return False
    
if __name__ == '__main__':
    Test()

