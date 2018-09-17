# Copyright (C) 2012 Gonzalo Odiard <gonzalo@laptop.org>
# Based in code from Flavio Danesse <fdanesse@activitycentral.com>
# and Ariel Calzada <ariel.calzada@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import shutil
from gettext import gettext as _

from gi.repository import GObject
from gi.repository import Gio

from sugar3.graphics.menuitem import MenuItem
from sugar3.graphics.toolbutton import ToolButton
from sugar3 import env

DEFAULT_FONTS = ['Sans', 'Serif', 'Monospace']
USER_FONTS_FILE_PATH = env.get_profile_path('fonts')
GLOBAL_FONTS_FILE_PATH = '/etc/sugar_fonts'


class FontButton(ToolButton):

    __gsignals__ = {
        'changed': (GObject.SignalFlags.RUN_LAST, None, []),
    }

    def __init__(self):
        ToolButton.__init__(self, icon_name='font-text',
                            tooltip=_('Select font'))
        self.connect('clicked', self.__font_selection_cb)

        context = self.get_pango_context()

        self._init_font_list()

        self._font_name = 'Sans'
        font_names = []

        for family in context.list_families():
            name = family.get_name()
            if name in self._font_white_list:
                font_names.append(name)

        for font_name in sorted(font_names):
            menu_item = MenuItem(font_name)
            markup = '<span font="%s">%s</span>' % (font_name, font_name)
            menu_item.get_children()[0].set_markup(markup)
            menu_item.connect('activate', self.__menu_activated, font_name)
            self.props.palette.menu.append(menu_item)
            menu_item.show()

        self.show()

    def __font_selection_cb(self, widget):
        if self.props.palette:
            if not self.props.palette.is_up():
                self.props.palette.popup(immediate=True,
                                         state=self.props.palette.SECONDARY)
            else:
                self.props.palette.popdown(immediate=True)
            return

    def __menu_activated(self, menu, font_name):
        self._font_name = font_name
        self.emit('changed')

    def set_font_name(self, font_name):
        self._font_name = font_name

    def get_font_name(self):
        return self._font_name

    def _init_font_list(self):
        self._font_white_list = []
        self._font_white_list.extend(DEFAULT_FONTS)

        # check if there are a user configuration file
        if not os.path.exists(USER_FONTS_FILE_PATH):
            # verify if exists a file in /etc
            if os.path.exists(GLOBAL_FONTS_FILE_PATH):
                shutil.copy(GLOBAL_FONTS_FILE_PATH, USER_FONTS_FILE_PATH)

        if os.path.exists(USER_FONTS_FILE_PATH):
            # get the font names in the file to the white list
            fonts_file = open(USER_FONTS_FILE_PATH)
            # get the font names in the file to the white list
            for line in fonts_file:
                self._font_white_list.append(line.strip())
            # monitor changes in the file
            gio_fonts_file = Gio.File.new_for_path(USER_FONTS_FILE_PATH)
            self.monitor = gio_fonts_file.monitor_file(
                Gio.FileMonitorFlags.NONE, None)
            self.monitor.set_rate_limit(5000)
            self.monitor.connect('changed', self._reload_fonts)

    def _reload_fonts(self, monitor, gio_file, other_file, event):
        if event != Gio.FileMonitorEvent.CHANGES_DONE_HINT:
            return
        self._font_white_list = []
        self._font_white_list.extend(DEFAULT_FONTS)
        fonts_file = open(USER_FONTS_FILE_PATH)
        for line in fonts_file:
            self._font_white_list.append(line.strip())
        # update the menu
        for child in self.props.palette.menu.get_children():
            self.props.palette.menu.remove(child)
            child = None
        context = self.get_pango_context()
        tmp_list = []
        for family in context.list_families():
            name = family.get_name()
            if name in self._font_white_list:
                tmp_list.append(name)
        for font_name in sorted(tmp_list):
            menu_item = MenuItem(font_name)
            markup = '<span font="%s">%s</span>' % (font_name, font_name)
            menu_item.get_children()[0].set_markup(markup)
            menu_item.connect('activate', self.__menu_activated, font_name)
            self.props.palette.menu.append(menu_item)
            menu_item.show()
        return False
