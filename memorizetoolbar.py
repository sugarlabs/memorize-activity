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

import gobject
from os.path import join, dirname

from gettext import gettext as _
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toolcombobox import ToolComboBox
from sugar.graphics.alert import Alert
from sugar.graphics.icon import Icon

import logging
from gobject import SIGNAL_RUN_FIRST, TYPE_PYOBJECT

_logger = logging.getLogger('memorize-activity')


class MemorizeToolbarBuilder(gobject.GObject):

    __gtype_name__ = 'MemoryToolbarBuilder'

    standard_game_names = ['Load demo games',
                           'addition',
                           'letters',
                           'sounds'
                           ]
    translated_game_names = [_('Load demo games'),
                             _('addition'),
                             _('letters'),
                             _('sounds')
                            ]

    __gsignals__ = {
    'game_changed': (SIGNAL_RUN_FIRST, None, 5 * [TYPE_PYOBJECT])
    }

    def __init__(self, activity):
        gobject.GObject.__init__(self)
        self.activity = activity
        self.toolbar = self.activity.get_toolbar_box().toolbar
        self.jobject = None

        # Change size combobox
        self._size_combo = ToolComboBox()
        self._sizes = ['4 X 4', '5 X 5', '6 X 6']
        for i, f in enumerate(self._sizes):
            self._size_combo.combo.append_item(i, f)
        self.size_handle_id = self._size_combo.combo.connect( \
                'changed', self._game_size_cb)
        self.toolbar.insert(self._size_combo, -1)
        self._size_combo.combo.set_active(0)

        # Change demo games combobox
        self._game_combo = ToolComboBox()
        for i, f in enumerate(self.standard_game_names):
            f = _(f)
            self._game_combo.combo.append_item(i, f)
        self._game_combo.combo.set_active(0)
        self._game_combo.combo.connect('changed', self._game_changed_cb)
        self.toolbar.insert(self._game_combo, -1)

        # Reset Button
        self._restart_button = ToolButton('game-new')
        self._restart_button.connect('clicked', self._game_reset_cb)
        self._restart_button.set_tooltip(_('Restart Game'))
        self._restart_button.set_sensitive(False)
        self.toolbar.insert(self._restart_button, -1)
        self._restart_button.show()

    def _game_reset_cb(self, widget):
        self._restart_button.set_sensitive(False)
        self.emit('game_changed', None, None, 'reset', None, None)

    def update_controls(self, active):
        self._size_combo.set_sensitive(active)
        self._game_combo.set_sensitive(active)
        self._restart_button.set_sensitive(active and
                self.activity.game.model.count > 0)

    def card_flipped(self, widget, identifier, signal=False):
        self._restart_button.set_sensitive(self.activity.game.model.count > 0)

    def _game_size_cb(self, widget):
        game_size = int(self._sizes[self._size_combo.combo.get_active()][0])
        self.emit('game_changed', None, game_size, 'size', None, None)

    def _game_changed_cb(self, combobox):
        if combobox.get_active() == 0:
            return
        if self.activity.game.model.is_demo:
            self._change_game()
        else:
            alert = Alert()
            alert.props.title = _('Discard your modified game?')
            icon = Icon(icon_name='dialog-ok')
            alert.add_button(1, _('Discard'), icon)
            icon = Icon(icon_name='dialog-cancel')
            alert.add_button(0, _('Do not discard'), icon)
            alert.connect('response', self._change_game_alert_cb)
            self.activity.add_alert(alert)

    def _change_game_alert_cb(self, alert, response_id):
        if alert is not None:
            self.activity.remove_alert(alert)
        if response_id == 1:
            self._change_game()

    def _change_game(self):
        current_game = self._game_combo.combo.get_active()
        game_name = self.standard_game_names[current_game]
        title = game_name
        game_size = int(self._sizes[self._size_combo.combo.get_active()][0])

        if game_name in self.translated_game_names:
            index = self.translated_game_names.index(game_name)
            game_name = self.standard_game_names[index]

        game_file = join(dirname(__file__), 'demos', game_name + '.zip')
        self._game_combo.combo.set_active(0)
        self.emit('game_changed', game_file, game_size, 'demo', title, None)

    def update_toolbar(self, widget, data, grid):
        size = data.get('size')
        self._size_combo.combo.handler_block(self.size_handle_id)
        size_index = self._sizes.index(size + ' X ' + size)
        self._size_combo.combo.set_active(int(size_index))
        self._size_combo.combo.handler_unblock(self.size_handle_id)
