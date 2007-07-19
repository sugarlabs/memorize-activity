import gtk
import os
import random
import hippo
import gobject
from threading import Thread

from model import Model
from model import Pair
from createtable import CreateTable
from svgcard import SvgCard

class Test(object):

    TARGET_TYPE_TEXT = 80
    TARGET_TYPE_JPG = 81
    TARGET_TYPE_AUDIO = 82
    mime_text = [( "text/plain", 0, TARGET_TYPE_TEXT )] 
    mime_img = [( "image/x-jpg", 0, TARGET_TYPE_JPG )]
    mime_snd = [( "image/x-audio", 0, TARGET_TYPE_AUDIO )] 

    def __init__(self):

        self.model = Model(os.path.dirname(__file__))
        
        vbox = hippo.CanvasBox(spacing=4,
            orientation=hippo.ORIENTATION_VERTICAL)

        hbox = hippo.CanvasBox(spacing=4,
                               orientation=hippo.ORIENTATION_HORIZONTAL)
    
        self.table = CreateTable()
        self.table.make_table(3)

        control = self.make_control()
        hbox.append(control, hippo.PACK_EXPAND)
        hbox.append(hippo.CanvasWidget(widget=self.table), hippo.PACK_END)

        canvas = hippo.Canvas()
        canvas.set_root(hbox)

        window = gtk.Window()
        window.connect('destroy', gtk.main_quit)
        window.connect('key-press-event', self.key_press_cb)
        window.add(canvas)
        window.show_all()

        gtk.gdk.threads_init()
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass
        
    def key_press_cb(self, window, event):
        if gtk.gdk.keyval_name(event.keyval) in ('Escape', 'q'):
            gtk.main_quit()

    def sendCallback(self, widget, context, selection, targetType, eventTime):
        if targetType == self.TARGET_TYPE_JPG:
            selection.set(selection.target, 8,
                          self.obj)
        elif targetType == self.TARGET_TYPE_TEXT:
            selection.set(selection.target, 8,
                          self.obj)
        elif targetType == self.TARGET_TYPE_AUDIO:
            selection.set(selection.target, 8,
                          self.obj)
            
    def make_control(self):
        vbox = hippo.CanvasBox(spacing=4,
            orientation=hippo.ORIENTATION_VERTICAL)

        game_box = hippo.CanvasBox(spacing=4,
                               orientation=hippo.ORIENTATION_HORIZONTAL)

        self.name = gtk.Entry()
        game_box.append(hippo.CanvasWidget(widget=self.name), hippo.PACK_EXPAND)
        
        self.save = gtk.Button(label='save')
        game_box.append(hippo.CanvasWidget(widget=self.save), hippo.PACK_EXPAND)
        self.save.connect('clicked', self.save_cb)
                        
        self.load = gtk.Button(label='load')
        game_box.append(hippo.CanvasWidget(widget=self.load), hippo.PACK_EXPAND)
        self.load.connect('clicked', self.load_cb)

        pair_box = hippo.CanvasBox(spacing=4,
                                   orientation=hippo.ORIENTATION_HORIZONTAL)

        self.imgdir = gtk.Button(label='imgdir')
        pair_box.append(hippo.CanvasWidget(widget=self.imgdir), hippo.PACK_EXPAND)
        self.imgdir.connect('clicked', self.imgdir_cb)

        self.filew = gtk.FileSelection("File selection")
        self.filew.ok_button.connect("clicked", self.file_ok_sel)
        
        self.filew.cancel_button.connect("clicked",
                                         lambda w: self.filew.destroy())   	    
        self.filew.set_filename("penguin.png")               

        self.imgrec = gtk.Button(label='imgrec')
        pair_box.append(hippo.CanvasWidget(widget=self.imgrec), hippo.PACK_EXPAND)
        self.imgrec.connect('clicked', self.imgrec_cb)

        self.snddir = gtk.Button(label='snddir')
        pair_box.append(hippo.CanvasWidget(widget=self.snddir), hippo.PACK_EXPAND)
        self.snddir.connect('clicked', self.snddir_cb)

        self.sndrec = gtk.Button(label='sndrec')
        pair_box.append(hippo.CanvasWidget(widget=self.sndrec), hippo.PACK_EXPAND)
        self.sndrec.connect('clicked', self.sndrec_cb)

        props = {}
        props['front_border'] = {'opacity':'1'}
        props['front_h_border'] ={'opacity':'1'}
        props['front_text']= {'card_text':'', 'card_line1':'', 'card_line2':'', 'card_line3':'', 'card_line4':''}
        buffer_card = SvgCard(-1, {'front_border':{'opacity':'0'}, 'front_h_border':{'opacity':'0.5'},
                                   'back_text':{'card_text':''}}, {}, None, 184)
        
        self.card = SvgCard(0, props, buffer_card.get_cache(), None, 184)
        self.card.connect("drag_data_get", self.sendCallback)
        self.card.drag_source_set(gtk.gdk.BUTTON1_MASK, self.mime_text,
                             gtk.gdk.ACTION_COPY)
            
        vbox.append(game_box, hippo.PACK_EXPAND)
        vbox.append(pair_box, hippo.PACK_EXPAND)
        vbox.append(hippo.CanvasWidget(widget=self.card), hippo.PACK_END)

        return vbox
        
    def load_cb(self, event):
        name = self.name.get_text()
        print 'load name=%s '%name
        self.model.read(name)
        print self.model.pairs
        
    def save_cb(self, event):
        name = self.name.get_text()
        print 'save name=%s '%name
        self.model.data['name']=name
        self.model.write()
        
    def imgdir_cb(self, event):
        self.filew.show()
        self.which = 0
        
    def imgrec_cb(self, event):
        self.camera.start()
        
    def snddir_cb(self, event):
        self.filew.show()
        self.which = 1
        
    def sndrec_cb(self, event):
        pass

    def file_ok_sel(self, w):
        if self.which == 0:
            print "Image: %s" % self.filew.get_filename()        
            self.card.jpeg = self.filew.get_filename()
            self.card.reset()
            self.card.flip()

            self.obj = self.filew.get_filename()
            self.card.drag_source_set(gtk.gdk.BUTTON1_MASK, self.mime_img,
                                      gtk.gdk.ACTION_COPY)

        elif self.which == 1:
            print "Sound: %s" % self.filew.get_filename()        
            self.card.jpeg = 'ohr.jpg'
            self.card.reset()
            self.card.flip()

            self.obj = self.filew.get_filename()
            self.card.drag_source_set(gtk.gdk.BUTTON1_MASK, self.mime_snd,
                                      gtk.gdk.ACTION_COPY)

        #pair = Pair()
        #id = '0'
        #model.pairs[id] = pair        
        #model.pairs[id].set_property('aimg', 'eva.png')
        self.filew.hide()

        
if __name__ == '__main__':
    Test()


        
