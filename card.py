# Copyright (C) 2007, 2008 One Laptop per Child
# Copyright (C) 2013, Ignacio Rodriguez
#
# Muriel de Souza Godoi - muriel@laptop.org
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

import logging
import cairo

from gi.repository import GLib
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import Gtk
from gi.repository import Pango
from gi.repository import PangoCairo

from sugar3.util import LRU
from sugar3.graphics import style

import face
import model

BORDER_WIDTH = style.zoom(10)


class Card(Gtk.EventBox):

    # Default properties
    default_props = {}
    default_props['back'] = {'fill_color': style.Color('#666666'),
                             'stroke_color': style.Color('#666666')}
    default_props['back_text'] = {'text_color': style.Color('#c7c8cc')}
    default_props['front'] = {'fill_color': style.Color('#4b4d4a'),
                              'stroke_color': style.Color('#111111')}
    default_props['front_text'] = {'text_color': '#ffffff'}

    def __init__(self, identifier, pprops, image_path, size,
                 bg_color='#000000', font_name=model.DEFAULT_FONT,
                 show_robot=True):
        Gtk.EventBox.__init__(self)
        logging.debug('Card image_path %s', image_path)
        self.bg_color = bg_color
        self.flipped = False
        self.id = identifier
        self._image_path = image_path
        self.jpeg = None
        self.size = size
        # animation data
        self._steps_scales = [0.66, 0.33, 0.1, 0.33, 0.66]
        self._animation_steps = len(self._steps_scales)
        self._on_animation = False
        self._animation_step = 0
        self.show_robot = show_robot

        self.text_layouts = [None, None]
        self.font_name = font_name
        self._highlighted = False

        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(bg_color))
        self.set_size_request(size, size)

        # Views properties
        views = ['back', 'back_text', 'front', 'front_text']
        self.pprops = pprops
        self.props = {}
        for view in views:
            self.props[view] = {}
            self.props[view].update(self.default_props[view])
            self.props[view].update(pprops.get(view, {}))

        self._cached_surface = {True: None, False: None}

        self.draw = Gtk.DrawingArea()
        self.draw.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(bg_color))
        self.draw.set_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self.draw.connect('draw', self.__draw_cb)
        self.draw.show_all()

        self.workspace = Gtk.VBox()
        self.workspace.add(self.draw)
        self.add(self.workspace)
        self.show_all()

    def resize(self, new_size):
        self.size = new_size
        self.set_size_request(self.size, self.size)
        self._cached_surface = {True: None, False: None}
        self.jpeg = None
        self.text_layouts = [None, None]

    def __draw_cb(self, widget, context):
        flipped = self.flipped
        highlighted = self._highlighted
        if self._on_animation:
            if self._animation_step > self._animation_steps // 2:
                flipped = not self.flipped

        if not self._cached_surface[flipped]:
            self._prepare_cached_surface(context, flipped)

        if self._on_animation:
            scale = self._steps_scales[self._animation_step]
            context.translate(0, self.size * (1 - scale) // 2)
            context.scale(1.0, scale)
            self._animation_step += 1
            highlighted = False

        context.set_source_surface(self._cached_surface[flipped])
        context.paint()

        if highlighted:
            radio = self.size // 3
            self.draw_round_rect(context, 0, 0, self.size, self.size, radio)
            context.set_source_rgb(1., 1., 1.)
            context.set_line_width(BORDER_WIDTH)
            context.stroke()

        return False

    def _prepare_cached_surface(self, context, flipped):
        self._cached_surface[flipped] = \
            context.get_target().create_similar(cairo.CONTENT_COLOR_ALPHA,
                                                self.size, self.size)
        cache_context = cairo.Context(self._cached_surface[flipped])

        if flipped:
            icon_data = self.props['front']
        else:
            icon_data = self.props['back']

        cache_context.save()
        radio = self.size // 3
        self.draw_round_rect(cache_context, 0, 0, self.size, self.size,
                             radio)
        r, g, b, a = icon_data['fill_color'].get_rgba()
        cache_context.set_source_rgb(r, g, b)
        cache_context.fill_preserve()

        r, g, b, a = icon_data['stroke_color'].get_rgba()
        cache_context.set_source_rgb(r, g, b)
        cache_context.set_line_width(BORDER_WIDTH)
        cache_context.stroke()
        cache_context.restore()

        text_props = self.props[flipped and 'front_text' or 'back_text']
        if self._image_path is not None:
            if self.jpeg is None:
                image_size = self.size - style.DEFAULT_SPACING * 2
                self.jpeg = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._image_path, image_size, image_size)

        if self.jpeg is not None and flipped:
            Gdk.cairo_set_source_pixbuf(
                cache_context, self.jpeg,
                style.DEFAULT_SPACING, style.DEFAULT_SPACING)
            cache_context.paint()

        elif text_props['card_text']:
            cache_context.save()
            layout = self.text_layouts[flipped]

            if not layout:
                layout = self.text_layouts[flipped] = \
                    self.create_text_layout(text_props['card_text'])

            width, height = layout.get_pixel_size()
            y = (self.size - height) // 2
            x = (self.size - width) // 2
            cache_context.set_source_rgb(1, 1, 1)
            cache_context.translate(x, y)
            PangoCairo.update_layout(cache_context, layout)
            PangoCairo.show_layout(cache_context, layout)
            cache_context.fill()
            cache_context.restore()

    def set_border(self, stroke_color, fill_color, full_animation=False):
        """
        style_color, fill_color: str with format #RRGGBB
        """
        self.props['front'].update({'fill_color': style.Color(fill_color),
                                    'stroke_color': style.Color(stroke_color)})
        self._cached_surface[True] = None

        if full_animation:
            if self.get_speak():
                # If we displayed the robot face, displayed the text
                self.jpeg = None
                self.props['front_text']['speak'] = False

        if not self.is_flipped():
            self.flip(full_animation)
        else:
            self.queue_draw()

    def set_image_path(self, image_path):
        self._image_path = image_path
        self.jpeg = None
        self._cached_surface[True] = None
        self.queue_draw()

    def get_image_path(self):
        return self._image_path

    def set_highlight(self, status, mouse=False):
        if self.flipped and mouse:
            return
        self._highlighted = status
        self.queue_draw()

    def flip(self, full_animation=False):
        if self.flipped:
            return

        if self.jpeg is None:
            if self.jpeg is not None:
                image_size = self.size - style.DEFAULT_SPACING * 2
                self.jpeg = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._image_path, image_size, image_size)

        if full_animation:
            if self.id != -1 and self.get_speak():
                speaking_face = face.acquire()
                if speaking_face:
                    image_size = self.size - style.DEFAULT_SPACING * 2
                    if self.show_robot:
                        self.jpeg = GdkPixbuf.Pixbuf.new_from_file_at_size(
                            'icons/speak.svg', image_size, image_size)
                    speaking_face.face.say(self.get_text())

            self._animation_step = 0
            self._on_animation = True
            self._animate_flip()
        else:
            self._finish_flip()

    def _animate_flip(self):
        if self._animation_step < self._animation_steps - 1:
            self.queue_draw()
            GLib.timeout_add(100, self._animate_flip)
        else:
            self._finish_flip()
        return False

    def _finish_flip(self):
        self._on_animation = False
        self.flipped = True
        self.queue_draw()

    def cement(self):
        if not self.get_speak():
            return

    def flop(self):
        self._animation_step = 0
        self._on_animation = True
        self._animate_flop()

    def _animate_flop(self):
        if self._animation_step < self._animation_steps - 1:
            self.queue_draw()
            GLib.timeout_add(100, self._animate_flop)
        else:
            self._finish_flop()
        return False

    def _finish_flop(self):
        self._on_animation = False
        self.flipped = False
        self.queue_draw()

    def is_flipped(self):
        return self.flipped or self._on_animation

    def get_id(self):
        return self.id

    def reset(self):
        if self.flipped:
            self.flop()

    def create_text_layout(self, text):
        key = (self.size, text)
        if key in _text_layout_cache:
            return _text_layout_cache[key]

        max_lines_count = len([i for i in text.split(' ') if i])

        for size in list(range(80, 66, -8)) + list(range(66, 44, -6)) + \
                list(range(44, 24, -4)) + list(range(24, 15, -2)) + list(range(15, 7, -1)):

            card_size = self.size - BORDER_WIDTH * 2
            layout = self.create_pango_layout(text)
            layout.set_width(PIXELS_PANGO(card_size))
            layout.set_wrap(Pango.WrapMode.WORD)
            desc = Pango.FontDescription(self.font_name + " " + str(size))
            layout.set_font_description(desc)

            if layout.get_line_count() <= max_lines_count and \
                    layout.get_pixel_size()[0] <= card_size and \
                    layout.get_pixel_size()[1] <= card_size:
                break

        if layout.get_line_count() > 1:
            # XXX for single line ALIGN_CENTER wrongly affects on text position
            # and also in some cases for multilined text
            layout.set_alignment(Pango.Alignment.CENTER)

        _text_layout_cache[key] = layout

        return layout

    def change_font(self, font_name):
        # remove from local cache
        self.text_layouts[self.flipped] = False
        text = self.props['front_text']['card_text']
        key = (self.size, text)
        if key in _text_layout_cache:
            del _text_layout_cache[key]

        self.font_name = font_name
        self._cached_surface[True] = None
        self.queue_draw()

    def set_background(self, color):
        self.bg_color = color
        self.draw.modify_bg(Gtk.StateType.NORMAL,
                            Gdk.color_parse(self.bg_color))

    def change_text(self, newtext):
        self.text_layouts[self.flipped] = None
        self.props['front_text']['card_text'] = newtext
        self._cached_surface[True] = None
        self.queue_draw()

    def get_text(self):
        return self.props['front_text'].get('card_text', '')

    def change_speak(self, value):
        self.props['front_text']['speak'] = value

    def get_speak(self):
        return self.props['front_text'].get('speak') or False

    def draw_round_rect(self, context, x, y, w, h, r):
        context.move_to(x + r, y)
        context.line_to(x + w - r, y)
        context.curve_to(x + w, y, x + w, y, x + w, y + r)
        context.line_to(x + w, y + h - r)
        context.curve_to(x + w, y + h, x + w, y + h, x + w - r, y + h)
        context.line_to(x + r, y + h)
        context.curve_to(x, y + h, x, y + h, x, y + h - r)
        context.line_to(x, y + r)
        context.curve_to(x, y, x, y, x + r, y)


def PIXELS_PANGO(x):
    return x * 1000


_text_layout_cache = LRU(50)
