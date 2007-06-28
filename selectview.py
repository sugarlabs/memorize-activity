import hippo
import os
import gobject
import gtk

from sugar.graphics import color

from selectentry import SelectEntry

class SelectView(gtk.ScrolledWindow):
    __gtype_name__ = 'SelectView'
    
    __gsignals__ = {
        'entry-selected': (gobject.SIGNAL_RUN_FIRST,
                           gobject.TYPE_NONE,
                           ([object]))
        }

    _SELECTED = 1000000
    _UNSELECTED = 3520189183
    def __init__(self, names):
        gtk.ScrolledWindow.__init__(self)

        root = hippo.CanvasBox()
        root.props.orientation = hippo.ORIENTATION_VERTICAL

        canvas = hippo.Canvas()
        canvas.set_root(root)        
        self.add_with_viewport(canvas)
        
        self.tiles = []
        self.turn = 0
        self.current = 0
        
        for name in names:
            entry = SelectEntry(name)
            entry.connect('button-press-event', self._button_press_cb)
            root.append(entry)
            if name == names[0]:
                self.current = entry            
                entry.props.background_color = self._SELECTED
                entry.emit_paint_needed(0, 0, -1, -1)
                
        canvas.show()
        
    def _button_press_cb(self, entry, event, data=None):
        entry.props.background_color = self._SELECTED 
        entry.emit_paint_needed(0, 0, -1, -1)
        
        self.current.props.background_color = self._UNSELECTED
        self.current.emit_paint_needed(0, 0, -1, -1)
        self.current = entry
        self.emit('entry-selected', entry)
        
