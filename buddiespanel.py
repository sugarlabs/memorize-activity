import gtk
import hippo
import math

from sugar.graphics.canvasicon import CanvasIcon
from sugar.graphics.xocolor import XoColor
from sugar.graphics import color
from sugar.graphics import style
from sugar.graphics import units


class BuddyPlayer(hippo.CanvasBox, hippo.CanvasItem):
    __gtype_name__ = 'BuddyPlayer'
    _BORDER_DEFAULT = units.points_to_pixels(1.0)
 
    def __init__(self, buddy, **kargs):
        hippo.CanvasBox.__init__(self, **kargs)
       
        self._radius = units.points_to_pixels(5)
        self.props.border_color = 0
        self.props.background_color = 0
        self.props.orientation = hippo.ORIENTATION_VERTICAL
        self.props.border = self._BORDER_DEFAULT
        self.props.border_left = self._radius
        self.props.border_right = self._radius
        
        buddy_color = buddy.props.color
        if not buddy_color:
            buddy_color = "#000000,#ffffff"

        self.icon = CanvasIcon(
            icon_name='theme:stock-buddy',
            xo_color=XoColor(buddy_color))

        nick = buddy.props.nick
        if not nick:
            nick = ""
        self.name = hippo.CanvasText(text=nick, size_mode=hippo.CANVAS_SIZE_WRAP_WORD, color=color.WHITE.get_int())

        self.append(self.icon)
        self.append(self.name)

        
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


class BuddiesPanel(hippo.CanvasBox):
    _COLOR_ACTIVE = 50
    _COLOR_INACTIVE = 0
    
    def __init__(self):
        hippo.CanvasBox.__init__(self, spacing=4, padding=5,
                orientation=hippo.ORIENTATION_VERTICAL)

        self.players_box = hippo.CanvasBox(spacing=4, padding=5,
                orientation=hippo.ORIENTATION_VERTICAL)

        self.watchers_box = hippo.CanvasBox(spacing=4, padding=5,
                orientation=hippo.ORIENTATION_VERTICAL)

        self.append(self.players_box)
        self.append(hippo.CanvasWidget(widget=gtk.HSeparator()))
        self.append(self.watchers_box, hippo.PACK_EXPAND)

        self.players = {}
        self.watchers = {}
        self.last_active = None
        
    def _create_buddy_vbox (self, buddy):
        buddy_color = buddy.props.color
        if not buddy_color:
            buddy_color = "#000000,#ffffff"

        icon = CanvasIcon(
            icon_name='theme:stock-buddy',
            xo_color=XoColor(buddy_color))

        nick = buddy.props.nick
        if not nick:
            nick = ""
        name = hippo.CanvasText(text=nick, color=color.WHITE.get_int())

        vbox = hippo.CanvasBox(padding=5)
        vbox._radius = units.points_to_pixels(5)
        vbox.props.border_color = 100
        vbox.props.background_color = 200
        vbox.props.orientation = hippo.ORIENTATION_VERTICAL
        vbox.props.border = units.points_to_pixels(1.0)
        vbox.props.border_left = vbox._radius
        vbox.props.border_right = vbox._radius

        vbox.append(icon)
        vbox.append(name)

        return vbox

    def add_watcher(self, buddy):
        op = buddy.object_path()
        if self.watchers.get(op) is not None:
            return
        # if the watcher is also a player, don't add them
        if self.players.get(op) is not None:
            return

        vbox = self._create_buddy_vbox (buddy)

        self.watchers_box.append(vbox)

        self.watchers[op] = vbox

    def add_player(self, buddy):
        op = buddy.object_path()
        if self.players.get(op) is not None:
            return
        # if the player is also a watcher, drop them from the watchers
        widget = self.watchers.pop(op, None)
        if widget is not None:
            self.watchers_box.remove(widget)

        assert len(self.players) < 2

        hbox = hippo.CanvasBox(spacing=4, padding=5,
                orientation=hippo.ORIENTATION_HORIZONTAL)
        hbox.append(BuddyPlayer(buddy))

        count_font = style.FONT_BOLD.get_pango_desc()
        count_font.set_size(30000)
        count = hippo.CanvasText(text="0", color=color.WHITE.get_int(),
                font_desc=count_font)
        hbox.append(count)

        self.players_box.append(hbox)

        self.players[op] = hbox
        
    def set_is_playing(self, buddy):
        hbox = self.players.get(buddy.object_path())
        bp = hbox.get_children()[0]
        bp.props.background_color = self._COLOR_ACTIVE
        bp.emit_paint_needed(0, 0, -1, -1)
        if self.last_active is not None:
            hbox = self.players.get(self.last_active.object_path())
            lbp = hbox.get_children()[0]
            lbp.props.background_color = self._COLOR_INACTIVE
            lbp.emit_paint_needed(0, 0, -1, -1)
        self.last_active = buddy
    
    def set_count(self, buddy, val):
        hbox = self.players.get(buddy.object_path())
        if hbox is None:
            return

        count = hbox.get_children()[1]
        count.props.text = str(val)

    def remove_watcher(self, buddy):
        op = buddy.object_path()
        widget = self.watchers[op]
        if widget is None:
            return

        self.watchers_box.remove(widget)
        del self.watchers[op]

        # removing someone from the game entirely should also remove them
        # from the players
        self.remove_player(buddy)

    def remove_player(self, buddy):
        op = buddy.object_path()
        widget = self.players.get(op)
        if widget is None:
            return

        self.players_box.remove(widget)
        del self.players[op]

        self.add_watcher(buddy)
