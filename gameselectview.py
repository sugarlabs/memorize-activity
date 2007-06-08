import hippo
import os
import gobject
import gtk

from sugar.graphics import color

from gameobject import GameObject

class GameSelectView(gtk.ScrolledWindow):
    __gtype_name__ = 'GameSelectView'
    
    __gsignals__ = {
        'entry-selected': (gobject.SIGNAL_RUN_FIRST,
                           gobject.TYPE_NONE,
                           ([object]))
        }
        
    def __init__(self, name):
        gtk.ScrolledWindow.__init__(self)

        root = hippo.CanvasBox()
        root.props.orientation = hippo.ORIENTATION_VERTICAL

        canvas = hippo.Canvas()
        canvas.set_root(root)        
        self.add_with_viewport(canvas)
        
        self.tiles = []
        self.turn = 0
        self.current = 0
        
        tile_num = 0
        numtiles = 2
        while tile_num < numtiles:
            
            entry = GameObject(name[tile_num])
            entry.connect('button-press-event', self._button_press_cb)
            root.append(entry)
            self.current = entry
            tile_num+=1

        canvas.show()
        
    def _button_press_cb(self, entry, event, data=None):
        entry.props.background_color = 1000
        entry.emit_paint_needed(0, 0, -1, -1)
        
        self.current.props.background_color = 1000000
        self.current.emit_paint_needed(0, 0, -1, -1)
        self.current = entry
        self.emit('entry-selected', entry)
        
