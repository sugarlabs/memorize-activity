import gtk
import hippo
import math
import os

from sugar.graphics import units

class PlayTile(hippo.CanvasBox, hippo.CanvasItem):
    __gtype_name__ = 'PlayTile'
    _BORDER_DEFAULT = units.points_to_pixels(1.0)
 
    def __init__(self, num, **kargs):
        hippo.CanvasBox.__init__(self, **kargs)

        self.num = num
        self.image = os.path.join(os.path.dirname(__file__), 'images/black.png')
        
        self._radius = units.points_to_pixels(5)
        self.props.border_color = 100
        self.props.background_color = 100
        self.props.orientation = hippo.ORIENTATION_VERTICAL
        self.props.border = self._BORDER_DEFAULT
        self.props.border_left = self._radius
        self.props.border_right = self._radius
        
        self.append(self._build_title_box())

        
    def do_paint_background(self, cr, damaged_box):
        [width, height] = self.get_allocation()     

        x = self._BORDER_DEFAULT / 2
        y = self._BORDER_DEFAULT / 2
        width -= self._BORDER_DEFAULT
        height -= self._BORDER_DEFAULT

        cr.move_to(x + self._radius, y);
        cr.arc(x + width - self._radius, y + self._radius,
               self._radius, math.pi * 1.5, math.pi * 2);
        cr.arc(x + width - self._radius, x + height - self._radius,
               self._radius, 0, math.pi * 0.5);
        cr.arc(x + self._radius, y + height - self._radius,
               self._radius, math.pi * 0.5, math.pi);
        cr.arc(x + self._radius, y + self._radius, self._radius,
               math.pi, math.pi * 1.5);

        hippo.cairo_set_source_rgba32(cr, self.props.background_color)
        cr.fill()
        
    def _build_title_box(self):
        hbox = hippo.CanvasBox(orientation=hippo.ORIENTATION_HORIZONTAL)
        hbox.props.spacing = units.points_to_pixels(5)
        hbox.props.padding_top = units.points_to_pixels(5)
        hbox.props.padding_bottom = units.points_to_pixels(5)
                
        self.img_widget = gtk.Image()
        self.img_pixbuf = gtk.gdk.pixbuf_new_from_file(self.image)
        self.img_widget.set_from_pixbuf(self.img_pixbuf)

        canvas_widget = hippo.CanvasWidget()
        canvas_widget.props.widget = self.img_widget
        self.img_widget.show()
        hbox.append(canvas_widget)
        
        return hbox



