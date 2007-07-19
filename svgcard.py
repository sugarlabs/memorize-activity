#! /usr/bin/env python
#
#    Copyright (C) 2007, One Laptop Per Child
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

import os
import gc
import rsvg
import re
import svglabel
import gtk
import gobject
import pango

class SvgCard(gtk.DrawingArea):
        
    border_svg = os.path.join(os.path.dirname(__file__), "images/card.svg")
    text_svg = os.path.join(os.path.dirname(__file__), "images/card-text.svg")
               
    # Default properties
    default_props = {}
    default_props['back_border'] = {'filename':border_svg, 'fill_color':'#b2b3b7', 'stroke_color':'#b2b3b7', 'opacity':'1'}
    default_props['back_h_border'] = {'filename':border_svg, 'fill_color':'#b2b3b7', 'stroke_color':'#ffffff', 'opacity':'1'}
    default_props['back_text'] = {'filename':text_svg, 'text_color':'#c7c8cc'}
    default_props['front_border'] = {'filename':border_svg, 'fill_color':'#4c4d4f', 'stroke_color':'#ffffff', 'opacity':'0'}
    default_props['front_h_border'] = {'filename':border_svg, 'fill_color':'#555555', 'stroke_color':'#888888', 'opacity':'0.5'}
    default_props['front_text'] = {'filename':text_svg, 'text_color':'#ffffff'}

    
    def __init__(self, id, pprops, pcache, jpeg, size):
        gtk.DrawingArea.__init__(self)
        self.set_size_request(size, size)
        self.bg_color = '#000000'
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.bg_color))
        self.connect('expose-event', self._expose_cb)        
        self.flipped = False
        self.id = id      
        self.jpeg = jpeg
        self.size = size
        self.set_flags(gtk.CAN_FOCUS)
                
        # Views properties
        views = ['back_border','back_h_border','back_text','front_border','front_h_border','front_text']
        self.pprops = pprops
        self.props = {}
        for view in views:
            self.props[view] = {}
            self.props[view].update(self.default_props[view])
            self.props[view].update(pprops.get(view, {}))

        # Cache
        self.cache = {} 
        self.cache.update(pcache)

        if len(self.cache) == 0:
            build_all = True
        else:
            build_all = False
        
        self.build_all = build_all
        
        if build_all or pprops.has_key('back_border'):
            self.cache['back_border']= self._read_icon_data(self.props['back_border'])
        if build_all or pprops.has_key('back_h_border'):
            self.cache['back_h_border']= self._read_icon_data(self.props['back_h_border'])
        if build_all or pprops.has_key('back_text'):
            #text = CardText(self.props['back_text'].get('card_text', ''), self.props['back_text'].get('text_color'))
            text = self._read_icon_data(self.props['back_text'])
            self.cache['back_text'] = text.scale_simple(self.size-14, self.size-14, gtk.gdk.INTERP_BILINEAR)
            del text
        self.back_layout = self.get_text_layout(self.props['back_text'].get('card_text', ''), self.size-12)
        self.back_layout_position = (self.size -(self.back_layout.get_size()[1]/1000))/2
        self.current_layout_position = self.back_layout_position
        self.current_text_color = self.props['back_text'].get('text_color','#c7c8cc')
        if build_all or self.pprops.has_key('back_border') or self.pprops.has_key('back_text'):
            self.cache['back'] = self.build_face('back')
        if build_all or self.pprops.has_key('back_h_border') or self.pprops.has_key('back_text'):
            self.cache['back_h'] = self.build_face('back_h')
        
        self.current_pixbuf = self.cache['back']
        self.current_layout = self.back_layout
        # Set events and listeners
        self.set_events(gtk.gdk.ALL_EVENTS_MASK)
        gc.collect()
        self.show()

    def _expose_cb(self, widget, event):
        self.window.draw_pixbuf(None, self.current_pixbuf, 0, 0, 0, 0)
        gc = self.window.new_gc()
        widget.window.draw_layout(gc, x=6, y=self.current_layout_position, layout=self.current_layout, foreground=gtk.gdk.color_parse(self.current_text_color))
        return False

    def _read_icon_data(self, dict):
        icon_file = open(dict.get('filename', 'card.svg'), 'r')
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

        # Replace text parameters
        entity = '<!ENTITY text_color "%s">' % dict.get('text_color', '#ffffff')
        data = re.sub('<!ENTITY text_color .*>', entity, data)

        data = re.sub('card_text', dict.get('card_text', ''), data)
        data = re.sub('card_line1', dict.get('card_line1', ''), data)
        data = re.sub('card_line2', dict.get('card_line2', ''), data)
        data = re.sub('card_line3', dict.get('card_line3', ''), data)
        data = re.sub('card_line4', dict.get('card_line4', ''), data)

        self.data_size = len(data)
        return rsvg.Handle(data=data).get_pixbuf()
    
    def build_face(self, face):
        if face.endswith('_h'):
            text = face[:-2]
        else:
            text = face
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, self.size, self.size)
        pixbuf.fill(0x00000000)
        self.cache[face + '_border'].composite(pixbuf, 0, 0, self.size, self.size, 0, 0, 1, 1, gtk.gdk.INTERP_NEAREST, 255)
        if face.startswith('front') and self.jpeg <> None:
            self.cache['jpeg'].composite(pixbuf, 11, 11, self.size-22, self.size-22, 11, 11, 1, 1, gtk.gdk.INTERP_NEAREST, 255)
        #self.cache[face + '_border'].composite(pixbuf, 0, 0, self.size, self.size, 0, 0, 1, 1, gtk.gdk.INTERP_BILINEAR, 255)
        #self.cache[text + '_text'].composite(pixbuf, 11, 11, self.size-22, self.size-22, 11, 11, 1, 1, gtk.gdk.INTERP_NEAREST, 255)
        return pixbuf
    
    def set_border(self, stroke_color, fill_color):
        self.props['front_border'].update({'fill_color':fill_color, 'stroke_color':stroke_color})
        self.cache['front_border'] = self._read_icon_data(self.props['front_border'])
        self.cache['front'] = self.build_face('front')
        self.current_pixbuf = self.cache['front']
        self.queue_draw()      

    def set_highlight(self, status, mouse = False):
        if self.flipped:
            if mouse:
                return
            if status:
                self.current_pixbuf = self.cache['front_h']
            else:
                self.current_pixbuf = self.cache['front']
        else:  
            if status:
                self.current_pixbuf = self.cache['back_h']
            else:
                self.current_pixbuf = self.cache['back']    
        self.queue_draw()                 
            
    def flip(self):
        if self.build_all or self.pprops.has_key('front_border'):
            self.cache['front_border']= self._read_icon_data(self.props['front_border'])
        if self.build_all or self.pprops.has_key('front_h_border'):
            self.cache['front_h_border']= self._read_icon_data(self.props['front_h_border'])
        if self.build_all or self.pprops.has_key('front_text'):
            text = self._read_icon_data(self.props['front_text'])            
            self.cache['front_text'] = text.scale_simple(self.size-22, self.size-22, gtk.gdk.INTERP_BILINEAR)
            del text
        self.front_layout = self.get_text_layout(self.props['front_text'].get('card_text', ''), self.size-11)    
        self.front_layout_position = (self.size -(self.front_layout.get_size()[1]/1000))/2
        self.current_layout = self.front_layout
        self.current_layout_position = self.front_layout_position
        self.current_text_color = self.props['front_text'].get('text_color','#c7c8cc')
        if self.jpeg <> None:
            pixbuf_t = gtk.gdk.pixbuf_new_from_file(self.jpeg)
            # pixbuf_t = pixbuf_t.add_alpha(True,chr(255),chr(255),chr(255))
            self.cache['jpeg']= pixbuf_t.scale_simple(self.size-22, self.size-22, gtk.gdk.INTERP_BILINEAR)
            del pixbuf_t
            
        if self.cache.has_key('front_border') or self.cache.has_key('front_text'):
            self.cache['front'] = self.build_face('front')
        if self.cache.has_key('front_h_border') or self.cache.has_key('front_text'):
            self.cache['front_h'] = self.build_face('front_h')
            
        if not self.flipped:            
            self.current_pixbuf = self.build_face('front')
            self.flipped  = True
            self.queue_draw()
            while gtk.events_pending():
                gtk.main_iteration()    
    
    def flop(self):
        self.current_pixbuf = self.build_face('back')
        self.current_layout = self.back_layout
        self.current_layout_position = self.back_layout_position
        self.current_text_color = self.props['back_text'].get('text_color','#c7c8cc')
        self.flipped = False
        self.queue_draw()
        
    def is_flipped(self):
        return self.flipped
        
    def get_id(self):
        return self.id
    
    def get_cache(self):
        return self.cache
    
    def reset(self):
        if self.flipped:
            fill_color = self.default_props.get('front_border').get('fill_color')
            stroke_color = self.default_props.get('front_border').get('stroke_color')
            self.set_border(fill_color, stroke_color)
            self.flop()
            
    def get_text_layout(self, text, size):
        if self.size == 184:
            font_sizes = [50,40,26,20,17,13,11,8] 
        elif self.size == 145: 
            font_sizes = [45,28,20,16,13,11,9,8] 
        elif self.size == 119:
            font_sizes = [30,24,16,13,10,8,8,8] 

        # Set font size considering string length
        if len(text) <= 8:
            font_size = font_sizes[len(text)-1]
        else: 
            font_size = 8

        # Set Pango context and Pango layout
        context = self.create_pango_context()
        layout = self.create_pango_layout(text)
        desc = pango.FontDescription(' bold '+str(font_size))
        layout.set_font_description(desc)    
        layout.set_alignment(pango.ALIGN_CENTER)
        layout.set_width(size*1000)
        return layout
