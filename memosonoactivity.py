#! /usr/bin/env python
#
#    Copyright (C) 2006 Simon Schampijer
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

import gobject
import gtk, pygtk
import os
import socket
import logging
import random
import copy
import time
import errno
import gc

from sugar.activity.activity import Activity
from sugar.activity.activity import ActivityToolbox

from toolbar import ImageToolbar

from osc.oscapi import OscApi
from csound.csoundserver import CsoundServer
from gameselectview import GameSelectView

class MemosonoActivity(Activity):
    def __init__(self, handle):
        Activity.__init__(self, handle)
        self.set_title ("Memosono")

        toolbox = ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()
        #toolbox._notebook.connect('select-page', self._select_page)
        toolbox._notebook.connect('switch-page', self._switch_page)
        
        self.image_toolbar = ImageToolbar(toolbox)        
        toolbox.add_toolbar(_('Play'), self.image_toolbar)
        self.image_toolbar.show()

        self.gs = GameSelectView(['drumgit','summer'])
        self.gs.connect('entry-selected', self._entry_selected_cb)
        self.set_canvas(self.gs)
        self.gs.show()

        self.play = GameSelectView(['play', 'play'])
        
        '''
        # create our main abiword canvas
        self.abiword_canvas = Canvas()
        self.abiword_canvas.connect("can-undo", self._can_undo_cb)
        self.abiword_canvas.connect("can-redo", self._can_redo_cb)
        self.abiword_canvas.connect('text-selected', self._selection_cb)
        self.abiword_canvas.connect('image-selected', self._selection_cb)
        self.abiword_canvas.connect('selection-cleared', self._selection_cleared_cb)

        self._edit_toolbar = EditToolbar()

        self._edit_toolbar.undo.set_sensitive(False)
        self._edit_toolbar.undo.connect('clicked', self._undo_cb)

        self._edit_toolbar.redo.set_sensitive(False)
        self._edit_toolbar.redo.connect('clicked', self._redo_cb)

        self._edit_toolbar.copy.connect('clicked', self._copy_cb)
        self._edit_toolbar.paste.connect('clicked', self._paste_cb)

        toolbox.add_toolbar(_('Edit'), self._edit_toolbar)
        self._edit_toolbar.show()

        text_toolbar = TextToolbar(toolbox, self.abiword_canvas)
        toolbox.add_toolbar(_('Text'), text_toolbar)
        text_toolbar.show()

        image_toolbar = ImageToolbar(toolbox, self.abiword_canvas)
        toolbox.add_toolbar(_('Image'), image_toolbar)
        image_toolbar.show()

        table_toolbar = TableToolbar(toolbox, self.abiword_canvas)
        toolbox.add_toolbar(_('Table'), table_toolbar)
        table_toolbar.show()

        view_toolbar = ViewToolbar(self.abiword_canvas)
        toolbox.add_toolbar(_('View'), view_toolbar)
        view_toolbar.show()

        self.set_canvas(self.abiword_canvas)
        self.abiword_canvas.show()

        self.abiword_canvas.connect_after('map', self._map_cb)
        '''

    def _entry_selected_cb(self, list_view, entry):
        self.set_canvas(self.play)
        self.play.show()

        #def _select_page(self, notebook, move_focus, user_param1 ):
        #print '+++++ select page'
        
    def _switch_page(self, notebook, page, page_num, user_param1=None):
        
        print '+++++ switch page %s'%str(page_num)
        
     # def get_nth_page(page_num)
     # page_num :	the index of a page in the notebook
     # Returns :	the child widget, or None if page_num is out of bounds.
     
    def _cleanup_cb(self, data=None):
        pass
        #self.controler.oscapi.send(('127.0.0.1', 6783), "/CSOUND/quit", [])
        #self.controler.oscapi.iosock.close()
        #self.server.oscapi.iosock.close()
        #logging.debug(" Closed OSC sockets ")
        
    def _focus_in(self, event, data=None):
        pass
        #logging.debug(" Memosono is visible: Connect to the Csound-Server. ")
        #self.controler.oscapi.send(('127.0.0.1', 6783), "/CSOUND/connect", [])
        
    def _focus_out(self, event, data=None):
        pass
        #logging.debug(" Memosono is invisible: Close the connection to the Csound-Server. ")
        #self.controler.oscapi.send(('127.0.0.1', 6783), "/CSOUND/disconnect", [])
