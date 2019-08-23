# Speak.activity
# A simple front end to the espeak text-to-speech engine on the XO laptop
# http://wiki.laptop.org/go/Speak
#
# Copyright (C) 2008  Joshua Minor
# This file is part of Speak.activity
#
# Parts of Speak.activity are based on code from Measure.activity
# Copyright (C) 2007  Arjun Sarwal - arjun@laptop.org
#
#     Speak.activity is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Speak.activity is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Speak.activity.  If not, see <http://www.gnu.org/licenses/>.

# This code is a super-stripped down version of the waveform view from Measure

import cairo

from gi.repository import Gtk


class Mouth(Gtk.DrawingArea):
    def __init__(self, fill_color):

        Gtk.DrawingArea.__init__(self)

        self.fill_color = fill_color

        def realize_cb(widget):
            widget.connect("draw", self.draw_cb)
        self.connect("realize", realize_cb)

    def stop(self):
        pass

    def draw_cb(self, widget, cr):
        bounds = self.get_allocation()

        # disable antialiasing
        cr.set_antialias(cairo.ANTIALIAS_NONE)

        # background
        cr.set_source_rgba(*self.fill_color.get_rgba())
        cr.rectangle(0, 0, bounds.width, bounds.height)
        cr.fill()

        # draw the mouth
        volume = self.volume / 30000.
        mouthH = volume * bounds.height
        mouthW = volume ** 2 * (bounds.width / 2.) + bounds.width / 2.
        #        T
        #  L           R
        #        B
        Lx, Ly = bounds.width / 2 - mouthW / 2, bounds.height / 2
        Tx, Ty = bounds.width / 2, bounds.height / 2 - mouthH / 2
        Rx, Ry = bounds.width / 2 + mouthW / 2, bounds.height / 2
        Bx, By = bounds.width / 2, bounds.height / 2 + mouthH / 2
        cr.set_line_width(min(bounds.height / 10.0, 10))
        cr.move_to(Lx, Ly)
        cr.curve_to(Tx, Ty, Tx, Ty, Rx, Ry)
        cr.curve_to(Bx, By, Bx, By, Lx, Ly)
        cr.set_source_rgb(0, 0, 0)
        cr.close_path()
        cr.stroke()

        cr.fill()
