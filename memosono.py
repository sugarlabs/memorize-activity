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
                                                
import gobject
import gtk, pygtk
import os
import socket
import pango
from  osc.oscAPI import *
from osc.OSC import *
import logging
import popen2
import random
import copy
import time
import errno
from sugar.activity.Activity import Activity

class Server:
    def __init__(self, _MEMO, port):
        self.oscapi = OscApi()  
        self.oscrecv = self.oscapi.createListener('127.0.0.1', port)
        
        gobject.io_add_watch(self.oscrecv, gobject.IO_IN, self._handle_query)
        self.oscapi.bind(self._tile, '/MEMO/tile')
        self.compkey = ''
        self.key = ''
        self.tile = 0
        self.comtile = 0
        self.match = 0
        self.addresses = {}
        self.addresses['eva'] = ['127.0.0.1', port+1]
        self.addresses['simon'] = ['127.0.0.1', port+2]
        self.players = ['eva', 'simon']
        self.currentplayer = 0
        self.lastplayer = 0
        self.numplayers = _MEMO['_NUM_PLAYERS']
        self.count = 0
        self.numpairs = _MEMO['_NUM_GRIDPOINTS']/2
        
    def _handle_query(self, source, condition):
        data, address = source.recvfrom(1024)
        self.oscapi.recvhandler(data, address)
        return True
        
# OSC-METHODS:    
    def _tile(self, *msg):
        self.tile = msg[0][2]
        self.key = msg[0][3] 

        # send to other machines
        for i in self.addresses:
            if msg[1][0] == self.addresses[i][0]:
                if msg[1][1] != self.addresses[i][1]:
                    self.oscapi.sendMsg("/MEMO/tile", [self.tile, self.key],
                                        self.addresses[i][0], self.addresses[i][1])        
            else:
                ## logging.debug(" Send the stuff ")
                self.oscapi.sendMsg("/MEMO/tile", [self.tile, self.key],
                                    self.addresses[i][0], self.addresses[i][1])                        
        # match
        if self.compkey != '':
            if self.compkey == self.key:
                ## logging.debug(" Key matches ")
                self.match = 1
                self.count += 1                    
            else:
                ## logging.debug(" Key does NOT match ")
                self.match = 0
            self.lastplayer = self.currentplayer   
            if self.match == 0:
                if self.currentplayer == self.numplayers-1 :
                    self.currentplayer = 0
                else:
                    self.currentplayer+=1                    
                i = 0    
                for i in self.addresses:
                    self.oscapi.sendMsg("/MEMO/game/next",[self.players[self.currentplayer],
                                                           self.players[self.lastplayer]],
                                        self.addresses[i][0], self.addresses[i][1])                    
            i = 0            
            for i in self.addresses:
                self.oscapi.sendMsg("/MEMO/game/match", [self.match, self.players[self.lastplayer],
                                                         self.comtile, self.tile, self.count&self.numpairs],
                                    self.addresses[i][0], self.addresses[i][1])        
            self.compkey = ''
            self.comptile = 0
        else:    
            self.compkey = self.key
            self.comtile = self.tile
        
    
    
class Controler(gobject.GObject):
    __gsignals__ = {
        'fliptile': (gobject.SIGNAL_RUN_FIRST,
                    gobject.TYPE_NONE,
                    ([gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT])),
        'game': (gobject.SIGNAL_RUN_FIRST,
                     gobject.TYPE_NONE,
                     ([gobject.TYPE_PYOBJECT])),
        'updatepointsc': (gobject.SIGNAL_RUN_FIRST,
                 gobject.TYPE_NONE,
                 ([gobject.TYPE_PYOBJECT])),
        'nextc': (gobject.SIGNAL_RUN_FIRST,
                 gobject.TYPE_NONE,
                 ([gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT])),
        'addplayer': (gobject.SIGNAL_RUN_FIRST,
                 gobject.TYPE_NONE,
                 ([gobject.TYPE_PYOBJECT])),
        'gameinit': (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                ([gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT])),
        'tileflippedc': (gobject.SIGNAL_RUN_FIRST,
                     gobject.TYPE_NONE,
                     ([gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT])),
        }
    def __init__(self, _MEMO, port):
        gobject.GObject.__init__(self)
        self._MEMO = _MEMO
        self.sound = 0
        # OSC-communication
        self.oscapi = OscApi()
        self.replyaddr = (('127.0.0.1', port)) 
        self.serveraddr = (('127.0.0.1', port))        
        self.oscrecv = self.oscapi.createListener('127.0.0.1', port+1)
        gobject.io_add_watch(self.oscrecv, gobject.IO_IN, self._handle_query)
        self.oscapi.bind(self._addplayer, '/MEMO/addplayer')
        self.oscapi.bind(self._game_init, '/MEMO/init')
        self.oscapi.bind(self._tile, '/MEMO/tile')
        self.oscapi.bind(self._game_match, '/MEMO/game/match')
        self.oscapi.bind(self._game_next, '/MEMO/game/next')
        self.block = 0

        # CSOUND-communication        
        self.id = 0 ##FIXME give a significant number 

    def csconnect(self):
        i = 0
        self.cssock = socket.socket()
        if self.cssock: 
            while i < 3: 
                try:
                    self.cssock.connect(('127.0.0.1', 6783))
                    logging.info(" Connected to csound server.")
                    self.sound = 1        
                    i = 3                 
                except:
                    logging.error(" Can not connect to csound server. Try again")
                    time.sleep(1)
                    i += 1
                    if i == 3:
                        self.cssock.close()
                        logging.error(" There will be no sound for memosono.")
        else:                        
            mess = "csound.SetChannel('sfplay.%d.on', 1)\n" % self.id
            self.cssock.send(mess)        
                                              
        
    def init_game(self, playername, numplayers, gamename):
        self.emit('gameinit', playername, numplayers, gamename)
    
    def _handle_query(self, source, condition):
        data, self.replyaddr = source.recvfrom(1024)
        self.oscapi.recvhandler(data, self.replyaddr)            
        return True

# SLOTS:       
    def _user_input(self, widget, tile_number):
        if not self.block:
            self.emit('fliptile', tile_number, 0)        
        return False    
    def _tile_flipped(self, model, tile_number, pic, sound, requesttype, chosen_flag):
        if chosen_flag == 1:
            self.emit('game', 'Chosen already!')
        else:
            if sound is not '-1':
                self.emit('tileflippedc', tile_number, pic, sound)
                if self.sound is 1:
                    if os.path.exists(os.path.join(self._MEMO['_DIR_GSOUNDS'],sound)):
                        mess = "perf.InputMessage('i 108 0 3 \"%s\" %s 0.7 0.5 0')\n"%(
                            os.path.join(self._MEMO['_DIR_GSOUNDS'],sound),self.id)
                        self.cssock.send(mess)
                        logging.info(" Read file: "+os.path.join(self._MEMO['_DIR_GSOUNDS'],sound))
            else:
                logging.error(" Can not read file: "+os.path.join(self._MEMO['_DIR_GSOUNDS'],sound))
                                
            if requesttype == 0:
                self.oscapi.sendMsg("/MEMO/tile", [tile_number, pic], self.serveraddr[0], self.serveraddr[1])
        return False

# OSC-METHODS:   
    def _addplayer(self, *msg):
        logging.debug(" Addplayer ")

    def _game_init(self, *msg):
        self.init_game(msg[0][2], msg[0][3], msg[0][4])

    def _tile(self, *msg):
        self.emit('fliptile', msg[0][2], 1)        

    def _game_next(self, *msg):
        self.emit('nextc', msg[0][2], msg[0][3])

    def _game_match(self, *msg):
        # flag_match, playername, tile1, tile2
        logging.debug(msg)
        if msg[0][2] == 1:
            # update points
            self.emit('updatepointsc', msg[0][3])
            if not msg[0][6]:
                self.emit('game', 'Match!')
            else:
                self.block = 1
                self.emit('game', 'The end')
        else:
            requesttype = 2 # 0:normal, 1:setback
            self.emit('game', 'Pairs do not match!')
            self.emit('fliptile', int(msg[0][4]), requesttype)
            self.emit('fliptile', int(msg[0][5]), requesttype)        

    
class Model(gobject.GObject):
    __gsignals__ = {
        'tileflipped': (gobject.SIGNAL_RUN_FIRST,
                    gobject.TYPE_NONE,
                    ([gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT,
                      gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT])),
        'nextm': (gobject.SIGNAL_RUN_FIRST,
                  gobject.TYPE_NONE,
                  ([gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT,
                    gobject.TYPE_PYOBJECT])),
        'updatepointsm': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT])),
        }
    def __init__(self, grid):       
        gobject.GObject.__init__(self)
        # tile - key=id, pic, sound, flag_flipped                    
        self.tileg = []
        i = 0
        for elem in grid:
            self.tileg.append(elem)
            i+=1
        # player - key=name, picture, tiles_won, scores
        self.player = {}        
        self.player['eva'] = [0, ['player1_0.jpg', 'player1_0b.jpg'],['player1_1.jpg', 'player1_1b.jpg'],
                              ['player1_2.jpg', 'player1_2b.jpg'],['player2_3.jpg', 'player2_3b.jpg'],
                              ['player1_4.jpg', 'player1_4b.jpg'],['player1_5.jpg', 'player1_5b.jpg'],
                              ['player1_6.jpg', 'player1_6b.jpg'],['player1_7.jpg', 'player1_7b.jpg'],
                              ['player1_8.jpg', 'player1_8b.jpg']]
        self.player['simon'] = [0, ['player2_0.jpg', 'player2_0b.jpg'],['player2_1.jpg', 'player2_1b.jpg'],
                              ['player2_2.jpg', 'player2_2b.jpg'],['player2_3.jpg', 'player2_3b.jpg'],
                              ['player2_4.jpg', 'player2_4b.jpg'],['player2_5.jpg', 'player2_5b.jpg'],
                              ['player2_6.jpg', 'player2_6b.jpg'],['player2_7.jpg', 'player2_7b.jpg'],
                              ['player2_8.jpg', 'player2_8b.jpg']]
        # game
        self.numplayers = 2

# SLOTS:
    def _game_init(self, controler, playername, numplayers, gamename):
        ## logging.debug(" gameinit ")
        return False
    def _add_player():
        ## logging.debug(" addplayer ")
        return False
    def _flip_tile(self, controler, tile_number, requesttype):        
        if requesttype == 0 or requesttype == 1:
            if self.tileg[tile_number][2] == 0: # !!FIX - better switch                
                self.tileg[tile_number][2] = 1
                # --->view: number, pic, sound, requesttype, chosen 
                self.emit('tileflipped', tile_number, self.tileg[tile_number][0],
                          self.tileg[tile_number][1], requesttype,0)
            else:                
                self.emit('tileflipped', tile_number, self.tileg[tile_number][0],
                          self.tileg[tile_number][1], requesttype,1)
        else:
            # set tilestate back
            self.tileg[tile_number][2] = 0
            gobject.timeout_add(2000, self._reset, tile_number, requesttype)
        return False
    
    def _reset(self, tile_number, requesttype):
        self.emit('tileflipped', tile_number, '-1', '-1', requesttype, 0)
        return False
    
    def _next(self, controler, player, lastplayer):
        gobject.timeout_add(2000, self._next_delayed, player, lastplayer)
    def _next_delayed(self, player, lastplayer ):
        count1 = self.player[player][0]        
        count2 = self.player[lastplayer][0]
        self.emit('nextm', player, self.player[player][count1+1][1], lastplayer,self.player[lastplayer][count2+1][0])
        return False
    
    def _updatepoints(self, controler, player):
        self.player[player][0] += 1
        pic_id = self.player[player][0]
        self.emit('updatepointsm', player, self.player[player][pic_id+1][1])
            
class View:
    def __init__(self, controler, memosonoactivity, _MEMO):
        self._MEMO = _MEMO
        self.row1 = gtk.HBox(False, 0)
        memosonoactivity.add(self.row1)
        # create the grid
        self.imageObj = []
        self.buttonObj = []
        # create the players
        self.p_imageObj = {}
        self.p_fixedObj = {}
        
# SLOTS:
    def _game_init(self, controler, playername, numplayers, gamename):
        # Create a table for the grid 
        self.num_elem_x = 4
        self.num_elem_y = 4
        self.table = gtk.Table(self.num_elem_y, self.num_elem_x, True)
        self.row1.pack_start(self.table)

        # scale black
        self.scale_x = 200
        self.scale_y = 200
        self.pixbuf_i = gtk.gdk.pixbuf_new_from_file(os.path.join(self._MEMO['_DIR_IMAGES'],"black80.jpg"))
        self.scaledbuf_i = self.pixbuf_i.scale_simple(self.scale_x, self.scale_y, gtk.gdk.INTERP_BILINEAR)

        self.y = 0
        self.x = 0
        i = 0
        while(self.y < self.num_elem_y):
            while(self.x < self.num_elem_x):
                self.imageObj.append(gtk.Image())
                self.imageObj[i].set_from_pixbuf(self.scaledbuf_i)
                self.imageObj[i].show()
                self.buttonObj.append(gtk.Button())
                self.buttonObj[i].add(self.imageObj[i])            
                self.table.attach(self.buttonObj[i], self.x, self.x+1, self.y, self.y+1)
                self.x+=1
                i+=1
            self.x=0
            self.y+=1

        # Players
        self.pscale_x = 400
        self.pscale_y = 400       
        self.downbox = gtk.HBox(False, 0)                        
        self.playerbox = gtk.VBox(False, 0)                        
        self.p1 = 'eva'
        self.p2 = 'simon'        
        self.p_imageObj[self.p1] = gtk.Image()
        self.p_imageObj[self.p1].set_from_pixbuf(self.pixbuf("player1_0b.jpg",0, self.pscale_x, self.pscale_y))        
        self.p_fixedObj[self.p1] = gtk.Fixed()
        self.p_fixedObj[self.p1].set_size_request(self.pscale_x, self.pscale_y)
        self.p_fixedObj[self.p1].add(self.p_imageObj[self.p1])
        self.playerbox.pack_start(self.p_fixedObj[self.p1])
        
        self.p_imageObj[self.p2] = gtk.Image()
        self.p_imageObj[self.p2].set_from_pixbuf(self.pixbuf("player2_0.jpg",0, self.pscale_x, self.pscale_y))
        self.p_fixedObj[self.p2] = gtk.Fixed()
        self.p_fixedObj[self.p2].set_size_request(self.pscale_x, self.pscale_y)
        self.p_fixedObj[self.p2].add(self.p_imageObj[self.p2])
        self.playerbox.pack_start(self.p_fixedObj[self.p2])

        self.downbox.pack_start(self.playerbox)
        self.row1.pack_start(self.downbox)
        self.row1.show_all()
        return False

    def pixbuf(self, filename, pictype, pscale_x, pscale_y):
        if pictype is 1:
            self.ppixbuf_i = gtk.gdk.pixbuf_new_from_file(os.path.join(self._MEMO['_DIR_GIMAGES'],filename))             
        if pictype is 0:
            self.ppixbuf_i = gtk.gdk.pixbuf_new_from_file(os.path.join(self._MEMO['_DIR_IMAGES'],filename))
            
        self.pscaledbuf_i = self.ppixbuf_i.scale_simple(pscale_x, pscale_y, gtk.gdk.INTERP_BILINEAR)
        return self.pscaledbuf_i

    def _next(self, controler, playername, filename, lastplayer, lastfilename):
        self.p_imageObj[playername].set_from_pixbuf(self.pixbuf(filename, 0, self.pscale_x, self.pscale_y))
        self.p_imageObj[lastplayer].set_from_pixbuf(self.pixbuf(lastfilename, 0, self.pscale_x, self.pscale_y))
        return False

    def _updatepoints(self, controler, playername, pic):
        self.p_imageObj[playername].set_from_pixbuf(self.pixbuf(pic, 0, self.pscale_x, self.pscale_y))  
        return False
    
    def _tile_flipped(self, model, tile_number, pic, sound):    
        if pic == "-1":
            self.imageObj[tile_number].set_from_pixbuf(self.pixbuf("black80.jpg", 0, self.scale_x, self.scale_y))
        else:
            self.imageObj[tile_number].set_from_pixbuf(self.pixbuf(pic, 1, self.scale_x, self.scale_y))          
        return False
                                                
    def _game(self, controler, string):        
        return False
    

def read_config(filename, seed, numelems):
    temp = []
    grid = []
    # set random seed
    random.seed(seed)
    filecheck = filename.split('.')
    if filecheck[2] != 'mson':
        logging.error(' File format of %s'%filename)
        ## sys.exit()
    else:
        fd = open(filename, 'r')
        if fd == None:
            logging.error(' Reading setup file %s'%filename)
            ## sys.exit()
        else:
            logging.info(' Read setup for memosono from file %s'%filename)        
            line = fd.readline()
            while line:
                zw = line.split()
                zw.append(0)
                if len(zw) is not 0:
                    temp.append(zw)
                line = fd.readline()
            fd.close()
            # select randomly numelems of the list
            grid = random.sample(temp, numelems)
            # make a complete deepcopy of the list 
            # and concatenate it at the end grid.extend()
            tm = copy.deepcopy(grid)
            grid.extend(tm)
            # shuffle th grid elements
            random.shuffle(grid)        
            return grid

            
def pathes(filename):
    # read config file
    path = []
    gamename = filename 
    home = os.path.join(os.path.dirname(os.path.abspath(__file__)), "games")
    gamepath = os.path.join(home, gamename)
    logging.debug(gamepath)        
    if not os.path.exists(gamepath):
        logging.error(" Game path does NOT exist in the home folder ")
    else:    
        logging.debug(" Game path exist in the home folder ")
        configpath = os.path.join(gamepath, filename+".mson")
        if not os.path.exists(configpath):
            logging.error(" Config file does NOT exist: "+configpath)
            logging.error(" Did you name it correct, ending with .mson? ")
            #sys.exit() ##FIXME
        else:
            path.append(configpath)
            logging.debug(" Config file is placed in the folder ")
            imagespath = os.path.join(gamepath, "images")
            soundspath = os.path.join(gamepath, "sounds") 
            if os.path.exists(imagespath):
                logging.debug(" Set path for images: "+imagespath)
                path.append(imagespath)
            else:
                logging.error(" Path to images does NOT exist ")
                #sys.exit()    ##FIXME            
            if os.path.exists(soundspath):
                logging.debug(" Set path for sounds: "+soundspath)
                path.append(soundspath)
            else:    
                logging.error(" Path to images does NOT exist ")
                #sys.exit() ##FIXME
    return path 


class MemosonoActivity(Activity):
    def __init__(self):
        Activity.__init__(self)
        self.connect('destroy', self._cleanup_cb)
        
        self.gamename = 'test'
        self.set_title("Memosono - "+self.gamename)
        
        # set path
        _MEMO = {}
        _MEMO['_DIR_CSSERVER'] = os.path.join(os.path.dirname(__file__), "csserver")
        _MEMO['_DIR_IMAGES'] = os.path.join(os.path.dirname(__file__), "images")
        logging.error( os.path.dirname('.') )
        _MEMO['_DIR_SOUNDS'] = os.path.join(os.path.dirname(__file__), "sounds")
        path = pathes(self.gamename)
        _MEMO['_DIR_GIMAGES'] = path[1]
        _MEMO['_DIR_GSOUNDS'] = path[2]
        # read config
        seed = random.randint(0, 14567)
        _MEMO['_NUM_GRIDPOINTS'] = 16
        _MEMO['_NUM_ELEMS'] = 8
        grid = read_config(path[0], seed, _MEMO['_NUM_ELEMS'])
                    
        _MEMO['_NUM_PLAYERS'] = 2
        name_creator = 'eva' 

        sock_check = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 7000
        i=0
        while i < 5:
            try:
                sock_check.bind(('127.0.0.1', self.port))
                logging.debug(" Memosono-Server has port "+str(self.port) )
                i = 5
            except socket.error:             
                if errno.EADDRINUSE:
                    logging.debug(" Port in use. Try another one. "+str(self.port))
                    self.port+=1000
                    i+=1
                    if i is 5:
                        logging.debug(" No free port found. Memosono will NOT work.")
        sock_check.close()                
        
        self.controler = Controler(_MEMO, self.port)        
        self.server = Server(_MEMO, self.port)
        self.model = Model(grid)    
        self.view = View(self.controler, self, _MEMO)
        
# SLOTS connections:        
        self.model.connect('tileflipped', self.controler._tile_flipped)
        self.controler.connect('tileflippedc', self.view._tile_flipped)
        self.controler.connect('fliptile', self.model._flip_tile)
        self.controler.connect('addplayer', self.model._add_player)
        self.controler.connect('gameinit', self.model._game_init)
        self.controler.connect('gameinit', self.view._game_init)
        self.controler.connect('game', self.view._game)
        self.controler.connect('nextc', self.model._next)
        self.model.connect('nextm', self.view._next)
        self.controler.connect('updatepointsc', self.model._updatepoints)
        self.model.connect('updatepointsm', self.view._updatepoints)
        # connect to the in/out events of the memosono activity
        self.connect('focus_in_event', self._focus_in)
        self.connect('focus_out_event', self._focus_out)


        self.controler.init_game(name_creator, _MEMO['_NUM_PLAYERS'], self.gamename)
        i = 0
        while(i < _MEMO['_NUM_GRIDPOINTS']):
            self.view.buttonObj[i].connect('clicked', self.controler._user_input, i)
            i+=1
            
    def _cleanup_cb(self, data=None):
        self.controler.oscapi.ioSocket.close()
        self.server.oscapi.ioSocket.close()
        logging.debug(" Closed OSC sockets ")
        if self.controler.cssock is not None:
            self.controler.cssock.close()

    def _focus_in(self, event, data=None):
        logging.debug(" Memosono is visible: Connect to the Csound-Server. ")
        self.controler.csconnect()
    def _focus_out(self, event, data=None):
        logging.debug(" Memosono is invisible: Close the connection to the Csound-Server. ")
        if self.controler.cssock is not None:
            self.controler.cssock.close()            
