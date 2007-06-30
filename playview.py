import hippo
import os
import cairo
import gtk

from sugar.graphics import color
from sugar.graphics import font

from playtile import PlayTile

class PlayView(hippo.CanvasBox, hippo.CanvasItem):    
    def __init__(self, numtiles, **kargs):
        hippo.CanvasBox.__init__(self, **kargs)

        self.props.orientation = hippo.ORIENTATION_VERTICAL
                        
        self.tiles = []
        
        tile_num = 0

        while tile_num < numtiles:
            if tile_num == 0 or ((tile_num)%4) == 0:
                box = hippo.CanvasBox()
                box.props.orientation = hippo.ORIENTATION_HORIZONTAL
                self.append(box)
                
            tile = PlayTile(tile_num)                   
            self.tiles.append(tile)            
            box.append(tile)
        
            tile_num+=1                    
            
    def flip(self, tile_num, obj, color):    
        tile = self.tiles[tile_num]
        tile.img_pixbuf = gtk.gdk.pixbuf_new_from_file(obj)
        tile.img_widget.set_from_pixbuf(tile.img_pixbuf)
        tile.props.background_color = color
        tile.emit_paint_needed(0, 0, -1, -1)
        
