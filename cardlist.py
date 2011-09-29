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

import gtk
import svgcard
import logging
from os.path import join, basename
import shutil

from model import Pair

from gobject import SIGNAL_RUN_FIRST, TYPE_PYOBJECT

from sugar.graphics import style
from sugar.graphics.icon import Icon

import theme

_logger = logging.getLogger('memorize-activity')


class CardList(gtk.EventBox):

    __gsignals__ = {
        'pair-selected': (SIGNAL_RUN_FIRST, None, 9 * [TYPE_PYOBJECT]),
        'update-create-toolbar': (SIGNAL_RUN_FIRST, None, 3 * [TYPE_PYOBJECT]),
    }

    def __init__(self):
        gtk.EventBox.__init__(self)
        self.pairs = []
        self.current_pair = None
        self.current_game_key = None
        self.model = None
        self.pair_list_modified = False
        self.game_loaded = False

        self.vbox = gtk.VBox(False)

        fill_box = gtk.Label()
        fill_box.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#000000'))
        fill_box.show()
        self.vbox.pack_end(fill_box, True, True)

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add_with_viewport(self.vbox)
        scroll.set_border_width(0)
        scroll.get_child().modify_bg(gtk.STATE_NORMAL,
                                     gtk.gdk.color_parse('#000000'))
        self.add(scroll)
        self.show_all()

    def load_game(self, game):
        if self.game_loaded:
            return
        self.get_window().freeze_updates()
        self.model = game.model
        self.current_game_key = self.model.data['game_file']
        game_pairs = self.model.pairs
        game_data = self.model.data
        self.clean_list(load=True)
        for key in game_pairs:
            if game_pairs[key].props.aimg != None:
                aimg = gtk.gdk.pixbuf_new_from_file( \
                    join(self.model.data['pathimg'],
                         game_pairs[key].props.aimg))
            else:
                aimg = None

            if game_pairs[key].props.bimg != None:
                bimg = gtk.gdk.pixbuf_new_from_file( \
                    join(self.model.data['pathimg'],
                         game_pairs[key].props.bimg))
            else:
                bimg = None

            if game_pairs[key].props.asnd != None:
                asnd = join(self.model.data['pathsnd'],
                            game_pairs[key].props.asnd)
            else:
                asnd = None

            if game_pairs[key].props.bsnd != None:
                bsnd = join(self.model.data['pathsnd'],
                            game_pairs[key].props.bsnd)
            else:
                bsnd = None

            self.add_pair(None, game_pairs[key].props.achar,
                    game_pairs[key].props.bchar, aimg, bimg, asnd, bsnd,
                    game_pairs[key].props.aspeak, game_pairs[key].props.bspeak,
                    False, load=True)
        self.get_window().thaw_updates()
        self.emit('update-create-toolbar', self.model.data['name'],
                  self.model.data['equal_pairs'],
                  self.model.data['divided'])
        self.game_loaded = True

    def update_model(self, game_model):
        game_model.pairs = {}
        equal_pairs = game_model.data['equal_pairs'] == '1'
        game_model.create_temp_directories()
        temp_img_folder = join(game_model.temp_folder, 'images')
        temp_snd_folder = join(game_model.temp_folder, 'sounds')

        for pair in range(len(self.pairs)):
            pair_card = Pair()
            # achar
            achar = self.pairs[pair].get_text(1)
            if achar != '':
                pair_card.set_property('achar', achar)

            # bchar
            bchar = self.pairs[pair].get_text(2)
            if bchar != '':
                pair_card.set_property('bchar', bchar)

            # aspeak
            aspeak = self.pairs[pair].get_speak(1)
            pair_card.set_property('aspeak', aspeak)

            # bspeak
            bspeak = self.pairs[pair].get_speak(2)
            pair_card.set_property('bspeak', bspeak)

            # aimg
            aimg = self.pairs[pair].get_pixbuf(1)
            if aimg != None:
                if equal_pairs:
                    aimgfile = 'img' + str(pair) + '.jpg'
                else:
                    aimgfile = 'aimg' + str(pair) + '.jpg'
                pair_card.set_property('aimg', aimgfile)
                aimg.save(join(temp_img_folder, aimgfile), 'jpeg',
                          {'quality': '85'})
            # bimg
            bimg = self.pairs[pair].get_pixbuf(2)
            if bimg != None:
                if equal_pairs:
                    bimgfile = 'img' + str(pair) + '.jpg'
                else:
                    bimgfile = 'bimg' + str(pair) + '.jpg'
                pair_card.set_property('bimg', bimgfile)
                bimg.save(join(temp_img_folder, bimgfile), 'jpeg',
                          {'quality': '85'})

            # asnd
            asnd = self.pairs[pair].get_sound(1)
            logging.debug('update_model asnd %s', asnd)
            if asnd != None:
                pair_card.set_property('asnd', basename(asnd))
            # bsnd
            bsnd = self.pairs[pair].get_sound(2)
            logging.debug('update_model bsnd %s', bsnd)
            if bsnd != None:
                pair_card.set_property('bsnd', basename(bsnd))

            game_model.pairs[pair] = pair_card
        self.pair_list_modified = False

    def clean_list(self, button=None, load=False):
        if button != None:
            self.current_game_key = None
        map(lambda x: self.vbox.remove(x), self.pairs)
        del self.pairs
        self.pairs = []
        if not load:
            self.pair_list_modified = True
            self.model.mark_modified()

    def add_pair(self, widget, achar, bchar, aimg, bimg, asnd, bsnd,
            aspeak, bspeak, show=True, load=False):
        pair = CardPair(achar, bchar, aimg, bimg, asnd, bsnd, aspeak, bspeak)
        self.vbox.pack_end(pair, False, True)
        self.pairs.append(pair)
        pair.connect('pair-selected', self.set_selected)
        pair.connect('pair-closed', self.rem_pair)
        if not load:
            self.model.mark_modified()
            self.pair_list_modified = True
        if show:
            self.show_all()

    def rem_pair(self, widget, event):
        self.vbox.remove(widget)
        self.pairs.remove(widget)
        del widget
        self.model.mark_modified()
        self.emit('pair-selected', False, None, None, None, None, None, None,
                False, False)

    def set_selected(self, widget, event):
        if self.current_pair is not None:
            current_pair = self.current_pair
            current_pair.set_selected(False)
        self.current_pair = widget
        widget.set_selected(True)
        self.emit('pair-selected', True,
                self.current_pair.get_text(1),
                self.current_pair.get_text(2),
                self.current_pair.get_pixbuf(1),
                self.current_pair.get_pixbuf(2),
                self.current_pair.get_sound(1),
                self.current_pair.get_sound(2),
                self.current_pair.get_speak(1),
                self.current_pair.get_speak(2))

    def update_selected(self, widget, newtext1, newtext2, aimg, bimg,
            asnd, bsnd, aspeak, bspeak):
        self.current_pair.change_text(newtext1, newtext2)
        self.current_pair.change_pixbuf(aimg, bimg)
        self.current_pair.change_sound(asnd, bsnd)
        self.current_pair.change_speak(aspeak, bspeak)
        self.model.mark_modified()
        self.pair_list_modified = False


class CardPair(gtk.EventBox):

    __gsignals__ = {
        'pair-selected': (SIGNAL_RUN_FIRST, None, [TYPE_PYOBJECT]),
        'pair-closed': (SIGNAL_RUN_FIRST, None, [TYPE_PYOBJECT]),
    }

    def __init__(self, text1, text2=None, aimg=None, bimg=None,
            asnd=None, bsnd=None, aspeak=None, bspeak=None):
        gtk.EventBox.__init__(self)
        self.bg_color = '#000000'

        self.asnd = asnd
        self.bsnd = bsnd

        self.current_game_key = None

        row = gtk.HBox()
        row.props.border_width = 10
        row.props.spacing = 10

        self.bcard1 = svgcard.SvgCard(-1,
                {'front_text': {'card_text': text1,
                                'speak': aspeak,
                                'text_color': '#ffffff'},
                  'front': {'fill_color': '#4c4d4f',
                            'stroke_color': '#ffffff',
                            'opacity': '1'}},
                  None, theme.PAIR_SIZE, 1, self.bg_color)
        self.bcard1.flip()
        self.bcard1.set_pixbuf(aimg)
        align = gtk.Alignment(.5, .5, 0, 0)
        align.add(self.bcard1)
        row.pack_start(align)

        self.bcard2 = svgcard.SvgCard(-1,
                {'front_text': {'card_text': text2,
                                'speak': bspeak,
                                 'text_color': '#ffffff'},
                  'front': {'fill_color': '#4c4d4f',
                            'stroke_color': '#ffffff',
                            'opacity': '1'}},
                  None, theme.PAIR_SIZE, 1, self.bg_color)
        self.bcard2.flip()
        self.bcard2.set_pixbuf(bimg)
        align = gtk.Alignment(.5, .5, 0, 0)
        align.add(self.bcard2)
        row.pack_start(align)

        close_image = Icon(
                icon_name='remove',
                icon_size=gtk.ICON_SIZE_LARGE_TOOLBAR)
        align = gtk.Alignment(.5, .5)
        align.add(close_image)
        close_button = gtk.ToolButton()
        close_button.set_icon_widget(align)
        close_button.connect('clicked', self.emit_close)
        close_button.set_size_request(style.STANDARD_ICON_SIZE,
                style.STANDARD_ICON_SIZE)
        align = gtk.Alignment(.5, 0, 0, 0)
        align.add(close_button)
        row.pack_start(align, False)

        self.connect('button-press-event', self.emit_selected)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.bg_color))
        self.add(row)
        self.show_all()

    def emit_selected(self, widget, event):
        self.emit('pair-selected', self)

    def emit_close(self, widget):
        self.emit('pair-closed', self)

    def set_selected(self, status):
        if not status:
            self.bg_color = '#000000'
        else:
            self.bg_color = '#b2b3b7'

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.bg_color))
        self.bcard1.set_background(self.bg_color)
        self.bcard2.set_background(self.bg_color)

    def change_pixbuf(self, aimg, bimg):
        self.bcard1.set_pixbuf(aimg)
        self.bcard2.set_pixbuf(bimg)

    def change_text(self, text1, text2):
        self.bcard1.change_text(text1)
        self.bcard2.change_text(text2)

    def change_sound(self, asnd, bsnd):
        self.asnd = asnd
        self.bsnd = bsnd

    def get_text(self, card):
        if card == 1:
            return self.bcard1.get_text()
        else:
            return self.bcard2.get_text()

    def change_speak(self, aspeak, bspeak):
        self.bcard1.change_speak(aspeak)
        self.bcard2.change_speak(bspeak)

    def get_speak(self, card):
        if card == 1:
            return self.bcard1.get_speak()
        else:
            return self.bcard2.get_speak()

    def get_pixbuf(self, card):
        if card == 1:
            return self.bcard1.get_pixbuf()
        else:
            return self.bcard2.get_pixbuf()

    def get_sound(self, card):
        if card == 1:
            return self.asnd
        else:
            return self.bsnd
