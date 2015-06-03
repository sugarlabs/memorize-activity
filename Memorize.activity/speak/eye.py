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

import math

import cairo
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject


class Eye(Gtk.DrawingArea):
    def __init__(self, fill_color):
        Gtk.DrawingArea.__init__(self)
        self.frame = 0
        self.x, self.y = 0,0
        self.fill_color = fill_color


    def do_draw(self, context):
        self.frame += 1
        bounds = self.get_allocation()

        self.context = context
        self.context.set_antialias(cairo.ANTIALIAS_NONE)

        self.draw_eye(bounds)
        return True

    def draw_eye(self, bounds):
        eyeSize = min(bounds.width, bounds.height)
        outlineWidth = eyeSize/20.0
        pupilSize = eyeSize/10.0
        pupilX, pupilY = ((eyeSize / 2) + pupilSize * 2, eyeSize / 2)
        dX = pupilX - bounds.width/2.
        dY = pupilY - bounds.height/2.
        distance = math.sqrt(dX*dX + dY*dY)
        limit = eyeSize/2 - outlineWidth*2 - pupilSize
        if distance > limit:
            pupilX = bounds.width/2 + dX*limit/distance
            pupilY = bounds.height/2 + dY*limit/distance


        self.context.arc(bounds.width/2,bounds.height/2, eyeSize/2-outlineWidth/2, 0,360)
        self.context.set_source_rgb(1,1,1)
        self.context.fill()

        # outline
        self.context.set_line_width(outlineWidth)
        self.context.arc(bounds.width/2,bounds.height/2, eyeSize/2-outlineWidth/2, 0,360)
        self.context.set_source_rgb(0,0,0)
        self.context.stroke()

        # pupil
        self.context.arc(pupilX,pupilY,pupilSize,0,360)
        self.context.set_source_rgb(0,0,0)
        self.context.fill()