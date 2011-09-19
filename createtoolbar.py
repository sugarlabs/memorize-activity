#    Copyright (C) 2006, 2007, 2008 One Laptop Per Child
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

from gettext import gettext as _

import gtk
import gobject
from gobject import SIGNAL_RUN_FIRST, TYPE_PYOBJECT

from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toggletoolbutton import ToggleToolButton
from sugar.graphics.alert import Alert
from sugar.graphics.icon import Icon


class CreateToolbarBuilder(gobject.GObject):

    __gtype_name__ = 'CreateToolbar'

    __gsignals__ = {
        'create_new_game': (SIGNAL_RUN_FIRST, None, []),
        'create_equal_pairs': (SIGNAL_RUN_FIRST, None, [TYPE_PYOBJECT]),
    }

    def __init__(self, activity):
        gobject.GObject.__init__(self)
        self.activity = activity
        self.toolbar = self.activity.get_toolbar_box().toolbar

        self._equal_pairs = ToggleToolButton('pair-non-equals')
        self._equal_pairs.set_tooltip(_('Set equal pairs'))
        self._equal_pairs.connect('toggled', self._emit_equal_pairs)
        self.toolbar.insert(self._equal_pairs, -1)

        self._grouped = ToggleToolButton('grouped_game1')
        self._grouped.set_tooltip(_('Set grouped game'))
        self._grouped.connect('toggled', self._grouped_cb)
        self.toolbar.insert(self._grouped, -1)

        self._clear_button = ToolButton('edit-clear')
        self._clear_button.set_tooltip(_('Clear current game'))
        self._clear_button.connect('clicked', self._clear_game_bt)
        self.toolbar.insert(self._clear_button, -1)

        self.toolbar.show_all()

    def _add_widget(self, widget, expand=False):
        tool_item = gtk.ToolItem()
        tool_item.set_expand(expand)
        tool_item.add(widget)
        widget.show()
        self.toolbar.insert(tool_item, -1)
        tool_item.show()

    def _clear_game_bt(self, button):
        alert = Alert()
        alert.props.title = _('Clear all the tiles from the game?')
        icon = Icon(icon_name='dialog-ok')
        alert.add_button(1, _('Clear'), icon)
        icon = Icon(icon_name='dialog-cancel')
        alert.add_button(0, _('Do not clear'), icon)
        alert.connect('response', self._clear_game_alert_cb)
        self.activity.add_alert(alert)

    def _clear_game_alert_cb(self, alert, response_id):
        self.activity.remove_alert(alert)
        if response_id == 1:
            self._equal_pairs.set_active(False)
            self._grouped.set_active(False)
            self.emit('create_new_game')

    def update_controls(self, active):
        self._equal_pairs.set_sensitive(active)
        self._grouped.set_sensitive(active)
        self._clear_button.set_sensitive(active)

    def _emit_equal_pairs(self, widget):
        if self._equal_pairs.get_active():
            self._equal_pairs.set_named_icon('pair-equals')
            self._equal_pairs.set_tooltip(_('Set non equal pairs'))
            self.activity.game.model.data['equal_pairs'] = '1'
        else:
            self._equal_pairs.set_named_icon('pair-non-equals')
            self._equal_pairs.set_tooltip(_('Set equal pairs'))
            self.activity.game.model.data['equal_pairs'] = '0'
        self.emit('create_equal_pairs', self._equal_pairs.get_active())

    def _grouped_cb(self, widget):
        if self._grouped.get_active():
            self._grouped.set_named_icon('grouped_game2')
            self._grouped.set_tooltip(_('Set ungrouped game'))
            self.activity.game.model.data['divided'] = '1'
        else:
            self._grouped.set_named_icon('grouped_game1')
            self._grouped.set_tooltip(_('Set grouped game'))
            self.activity.game.model.data['divided'] = '0'

    def update_create_toolbar(self, widget, game_name, equal_pairs, grouped):
        self._equal_pairs.set_active(equal_pairs == '1')
        self._grouped.set_active(grouped == '1')
