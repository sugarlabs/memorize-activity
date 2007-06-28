import gtk
import hippo
from sugar.graphics.canvasicon import CanvasIcon
from sugar.graphics.xocolor import XoColor
from sugar.graphics import color
from sugar.graphics import font

class BuddiesPanel(hippo.CanvasBox):
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

        vbox = self._create_buddy_vbox(buddy)
        hbox.append(vbox)

        count_font = font.DEFAULT_BOLD.get_pango_desc()
        count_font.set_size(30000)
        count = hippo.CanvasText(text="0", color=color.WHITE.get_int(),
                font_desc=count_font)
        hbox.append(count)

        self.players_box.append(hbox)

        self.players[op] = hbox

    def set_is_playing(self, buddy):
        op = buddy.object_path()
        for player, hbox in self.players.items():
            vbox = hbox.get_children()[0]
            icon, name = vbox.get_children()
            if player == op:
                name.props.font_desc = font.DEFAULT_BOLD.get_pango_desc()
            else:
                name.props.font_desc = font.DEFAULT.get_pango_desc()

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
