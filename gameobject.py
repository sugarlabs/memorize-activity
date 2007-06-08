import logging
from gettext import gettext as _
import datetime

import hippo
import pango

from sugar.graphics.frame import Frame
from sugar.graphics.xocolor import XoColor
from sugar.graphics import font
from sugar.graphics import color
from sugar.graphics import units


class GameObject(Frame):
    _DATE_COL_WIDTH    = units.points_to_pixels(150)
    _BUDDIES_COL_WIDTH = units.points_to_pixels(60)

    def __init__(self, name):
        Frame.__init__(self)
        self.props.box_height = units.grid_to_pixels(1)
        self.props.spacing = units.points_to_pixels(5)        
        
        self.props.border_color = color.FRAME_BORDER.get_int()
        self.props.background_color = color.FRAME_BORDER.get_int()       
        
        title = hippo.CanvasText(text=name,
                                 xalign=hippo.ALIGNMENT_START,
                                 font_desc=font.DEFAULT_BOLD.get_pango_desc(),
                                 size_mode=hippo.CANVAS_SIZE_ELLIPSIZE_END)
        self.append(title)
       
