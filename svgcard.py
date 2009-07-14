#    Copyright (C) 2007, 2008 One Laptop Per Child
#
#    Muriel de Souza Godoi - muriel@laptop.org
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

from os.path import join, dirname
import gc
import rsvg
import re
import gtk
import pango
import logging

from sugar.util import LRU

import theme
import face
import speak.voice

_logger = logging.getLogger('memorize-activity')

class SvgCard(gtk.EventBox):

    border_svg = join(dirname(__file__), 'images', 'card.svg')

    # Default properties
    default_props = {}
    default_props['back'] = {'fill_color':'#b2b3b7', 'stroke_color':'#b2b3b7', 'opacity':'1'}
    default_props['back_h'] = {'fill_color':'#b2b3b7', 'stroke_color':'#ffffff', 'opacity':'1'}
    default_props['back_text'] = {'text_color':'#c7c8cc'}
    default_props['front'] = {'fill_color':'#4c4d4f', 'stroke_color':'#ffffff', 'opacity':'1'}
    default_props['front_h'] = {'fill_color':'#555555', 'stroke_color':'#888888', 'opacity':'1'}
    default_props['front_text'] = {'text_color':'#ffffff'}

    cache = {}

    def __init__(self, id, pprops, jpeg, size, align, bg_color='#000000'):
        gtk.EventBox.__init__(self)

        self.bg_color = bg_color
        self.flipped = False
        self.flipped_once = False
        self.id = id
        self.jpeg = jpeg
        self.show_jpeg = False
        self.show_text = False
        self.size = size
        self.align = align
        self.text_layouts = [None, None]

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(bg_color))
        self.set_size_request(size, size)

        # Views properties
        views = ['back', 'back_h', 'back_text', 'front', 'front_h', 'front_text']
        self.pprops = pprops
        self.props = {}
        for view in views:
            self.props[view] = {}
            self.props[view].update(self.default_props[view])
            self.props[view].update(pprops.get(view, {}))

        if len(self.props['back_text'].get('card_text', '')) > 0:
            self.show_text = True
        self.current_face = 'back'

        self.draw = gtk.DrawingArea()
        self.draw.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(bg_color))
        self.draw.set_events(gtk.gdk.ALL_EVENTS_MASK)
        self.draw.connect('expose-event', self._expose_cb)
        self.draw.connect('realize', self._realize_cb)
        self.draw.show_all()

        self.workspace = gtk.VBox()
        self.workspace.add(self.draw)
        self.add(self.workspace)
        self.show_all()

        #gc.collect()

    def _realize_cb(self, widget):
        self.gc = widget.window.new_gc()

    def _expose_cb(self, widget, event):
        pixbuf = self._read_icon_data(self.current_face)
        widget.window.draw_pixbuf(None, pixbuf, 0, 0, 0, 0)

        if self.show_jpeg:
            widget.window.draw_pixbuf(None, self.jpeg, 0, 0,
                    theme.SVG_PAD, theme.SVG_PAD)

        if self.show_text:
            props = self.props[self.flipped and 'front_text' or 'back_text']
            layout = self.text_layouts[self.flipped]

            if not layout:
                layout = self.text_layouts[self.flipped] = \
                        self.create_text_layout(props['card_text'])

            width, height = layout.get_pixel_size()
            y = (self.size - height)/2
            if self.flipped:
                if self.align == '2': # top
                    y = 0
                elif self.align == '3': # bottom
                    y = self.size - height

            widget.window.draw_layout(self.gc, layout=layout,
                    x=(self.size - width)/2, y=y,
                    foreground=gtk.gdk.color_parse(props['text_color']))

        return False

    def _read_icon_data(self, view):
        dict = self.props[view]
        set  = str(self.size)+dict.get('fill_color')+dict.get('stroke_color')
        if self.cache.has_key(set):
            return self.cache[set]

        icon_file = open(self.border_svg, 'r')
        data = icon_file.read()
        icon_file.close()

        # Replace borders parameters
        entity = '<!ENTITY fill_color "%s">' % dict.get('fill_color', '')
        data = re.sub('<!ENTITY fill_color .*>', entity, data)

        entity = '<!ENTITY stroke_color "%s">' % dict.get('stroke_color', '')
        data = re.sub('<!ENTITY stroke_color .*>', entity, data)

        entity = '<!ENTITY opacity "%s">' % dict.get('opacity', '')
        data = re.sub('<!ENTITY opacity .*>', entity, data)

        data = re.sub('size_card1', str(self.size), data)
        data = re.sub('size_card2', str(self.size-6), data)
        data = re.sub('size_card3', str(self.size-17), data)
        pixbuf = rsvg.Handle(data=data).get_pixbuf()
        self.cache[set] = pixbuf
        return pixbuf

    def set_border(self, stroke_color, fill_color):
        self.props['front'].update({'fill_color':fill_color, 'stroke_color':stroke_color})
        self.queue_draw()
        while gtk.events_pending():
            gtk.main_iteration()

    def set_pixbuf(self, pixbuf):
        if pixbuf == None:
            self.jpeg = None
            self.show_jpeg = False
        else:
            if self.jpeg != None:
                del self.jpeg

            self.jpeg = pixbuf
            del pixbuf
            self.show_jpeg = True

        self.queue_draw()
        while gtk.events_pending():
            gtk.main_iteration()

    def get_pixbuf(self):
        return self.jpeg

    def set_highlight(self, status, mouse = False):
        if self.flipped:
            if mouse:
                return
            if status:
                self.current_face = 'front_h'
            else:
                self.current_face = 'front'
        else:
            if status:
                self.current_face = 'back_h'
            else:
                self.current_face = 'back'
        self.queue_draw()

    def flip(self):
        if self.flipped:
            return

        if not self.flipped_once:
            if self.jpeg <> None:
                pixbuf_t = gtk.gdk.pixbuf_new_from_file(self.jpeg)
                if pixbuf_t.get_width() != self.size-22 or pixbuf_t.get_height() != self.size-22:
                    self.jpeg = pixbuf_t.scale_simple(self.size-22, self.size-22, gtk.gdk.INTERP_BILINEAR)
                    del pixbuf_t
                else:
                    self.jpeg = pixbuf_t
            self.flipped_once = True

        if self.jpeg <> None:
            self.show_jpeg = True
        text = self.props.get('front_text', {}).get('card_text', '')
        if text != None and len(text) > 0:
            self.show_text = True
        else:
            self.show_text = False

        if self.id != -1 and self.get_speak():
            speaking_face = face.acquire()
            if speaking_face:
                self._switch_to_face(speaking_face)
                speaking_face.face.status.voice = \
                        speak.voice.by_name(self.get_speak())
                speaking_face.face.say(self.get_text())

        self.current_face = 'front'
        self.flipped  = True
        self.queue_draw()

        while gtk.events_pending():
            gtk.main_iteration()

        #gc.collect()

    def cement(self):
        if not self.get_speak():
            return
        self._switch_to_face(self.draw)

    def flop(self):
        self.current_face = 'back'
        if len(self.props['back_text'].get('card_text', '')) > 0:
            self.show_text = True
        else:
            self.show_text = False
        self.flipped = False
        self.show_jpeg = False

        if self.id != -1 and self.get_speak():
            self._switch_to_face(self.draw)

        self.queue_draw()

    def _switch_to_face(self, widget):
        for i in self.workspace.get_children():
            self.workspace.remove(i)
        self.workspace.add(widget)
        widget.set_size_request(self.size, self.size)

    def is_flipped(self):
        return self.flipped

    def get_id(self):
        return self.id

    def reset(self):
        if self.flipped:
            fill_color = self.default_props.get('front_border').get('fill_color')
            stroke_color = self.default_propsfront_text.get('front_border').get('stroke_color')
            self.set_border(fill_color, stroke_color)
            self.flop()

    def create_text_layout(self, text):
        key = (self.size, text)
        if key in _text_layout_cache:
            return _text_layout_cache[key]

        max_lines_count = len([i for i in text.split(' ') if i])

        for size in range(80, 66, -8) + range(66, 44, -6) + \
                range(44, 24, -4) + range(24, 15, -2) + range(15, 7, -1):

            card_size = self.size - theme.SVG_PAD*2
            layout = self.create_pango_layout(text)
            layout.set_width(PIXELS_PANGO(card_size))
            layout.set_wrap(pango.WRAP_WORD)
            desc = pango.FontDescription('Deja Vu Sans bold ' + str(size))
            layout.set_font_description(desc)

            if layout.get_line_count() <= max_lines_count and \
                    layout.get_pixel_size()[0] <= card_size and \
                    layout.get_pixel_size()[1] <= card_size:
                break

        if layout.get_line_count() > 1:
            # XXX for single line ALIGN_CENTER wrongly affects on text position
            # and also in some cases for multilined text
            layout.set_alignment(pango.ALIGN_CENTER)

        _text_layout_cache[key] = layout

        return layout

    def set_background(self, color):
        self.bg_color = color
        self.draw.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.bg_color))

    def change_text(self, newtext):
        self.text_layouts[self.flipped] = None
        self.props['front_text']['card_text'] = newtext
        if len(newtext) > 0:
            self.show_text = True
        self.queue_draw()

    def get_text(self):
        return self.props['front_text'].get('card_text', '')

    def change_speak(self, value):
        self.props['front_text']['speak'] = value

    def get_speak(self):
        return self.props['front_text'].get('speak')

def PIXELS_PANGO(x):
    return x * 1000

_text_layout_cache = LRU(50)
