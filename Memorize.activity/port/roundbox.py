import math

from gi.repository import Gtk

from sugar3.graphics import style


class RoundBox(Gtk.HBox):
    __gtype_name__ = 'RoundBox'

    _BORDER_DEFAULT = style.LINE_WIDTH

    def __init__(self, **kwargs):
        Gtk.HBox.__init__(self, **kwargs)

        self._radius = style.zoom(10)
        self.border = self._BORDER_DEFAULT
        self.border_color = style.COLOR_BLACK
        self.background_color = None
        self.connect("draw", self.__draw_cb)
        self.connect("size-allocate", self.__size_allocate_cb)
        self.connect("add", self.__add_cb)

    def __add_cb(self, child, params):
        child.set_border_width(style.zoom(5))

    def __size_allocate_cb(self, widget, allocation):
        self._x = allocation.x
        self._y = allocation.y
        self._width = allocation.width
        self._height = allocation.height

    def __draw_cb(self, widget, cr):
        x = self._x + self._BORDER_DEFAULT / 2
        y = self._y + self._BORDER_DEFAULT / 2
        width = self._width - self._BORDER_DEFAULT
        height = self._height - self._BORDER_DEFAULT

        cr.move_to(x + self._radius, y)
        cr.arc(x + width - self._radius, y + self._radius,
               self._radius, math.pi * 1.5, math.pi * 2)
        cr.arc(x + width - self._radius, y + height - self._radius,
               self._radius, 0, math.pi * 0.5)
        cr.arc(x + self._radius, y + height - self._radius,
               self._radius, math.pi * 0.5, math.pi)
        cr.arc(x + self._radius, y + self._radius, self._radius,
               math.pi, math.pi * 1.5)
        cr.close_path()

        if self.background_color is not None:
            r, g, b, a = self.background_color.get_rgba()
            cr.set_source_rgb(r, g, b)
            cr.fill_preserve()

        if self.border_color is not None:
            r, g, b, a = self.border_color.get_rgba()
            cr.set_source_rgb(r, g, b)
            cr.set_line_width(self.border)
            cr.stroke()
        #cr.restore()
            
if __name__ == '__main__':

    win = Gtk.Window()
    win.connect('destroy', Gtk.main_quit)
    win.set_default_size(450, 550)
    vbox = Gtk.VBox()

    box1 = RoundBox()
    vbox.add(box1)
    label1 = Gtk.Label(label="Test 1")
    box1.add(label1)

    rbox = RoundBox()
    rbox.background_color = style.Color('#FF0000')
    vbox.add(rbox)
    label2 = Gtk.Label(label="Test 2")
    rbox.add(label2)

    bbox = RoundBox()
    bbox.background_color = style.Color('#aaff33')
    bbox.border_color = style.Color('#ff3300')
    vbox.add(bbox)

    win.add(vbox)    
    win.show_all()
    Gtk.main()
