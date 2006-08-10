#!/usr/bin/python2.4
###########################
# Memoson
# Messages have the following appaerance:
# message type: name player: N/R: arg(n): arg(n+1)
#
# ports:
# csound server: 40002
# multicast: 40003
# ack (unicast): 40004
###########################

import select
import socket
import random
import pygtk
pygtk.require('2.0')
import gtk, gobject
import sys
import os
import pango
import time
from sugar.activity.Activity import Activity


class Communication(gobject.GObject):
    __gsignals__ = {
        'recvdata': (gobject.SIGNAL_RUN_FIRST,
                     gobject.TYPE_NONE,
                     ([gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT]))
        }
            
    def __init__(self, interface, maddr, port, numplayers, player, user_data=None):
        gobject.GObject.__init__(self)                    
        self.interface = interface
        self.maddr = maddr
        self.port = port
        self.addr_port = ((maddr, port))
        # create receiver and sender
        self.interface = interface
        self.openSockMultiRecv(maddr)
        self.openSockMultiSend()
        # no friends yet
        self.numplayers = numplayers
        self.player = player
        self.notfound = 1
        self.members = [[],[]]
        self.playlist = []
        self.sequence = -1
        # ports for ack        
        self.openAckSend()
        self.ackport = 40004
        self.ackaddr = ((self.interface, self.ackport))
        self.openAckRecv(self.ackaddr)
        # start the communication 
        self.start()

    def __del__(self):
        # close the multicast sockets
        self.closeSockMultiSend()
        self.closeSockMultiSend()
        
    def openSockMultiSend(self):
        self.socksend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Make the socket multicast-aware, and set TTL.
        self.socksend.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1) # set TTL

    def openSockMultiRecv(self, maddr):
        self.sockrecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # allow multiple connections form the same machine
        # several aplications can reuse the port - after restart the server do not have to wait
        self.sockrecv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
        # set the time to live (TTL) to one
        # only machines in the subnet will receive the packet
        self.sockrecv.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 1)
        # to allow to receive our own messages
#        self.sockrecv.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)                                    
    
    def start(self):
        """Let the listener socket start listening for network data."""
        self.sockrecv.bind(('', self.port))
        self.sockrecv.settimeout(2)
        # set the interface you want to use, the real machine address,
        # a multicast group address is a virtual address
        self.sockrecv.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self.interface))
        # join the multicast group
        self.sockrecv.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                                 socket.inet_aton(self.maddr) + socket.inet_aton(self.interface))        
        # Watch the listener socket for data
        # gobject.io_add_watch(fd, condition, callback, ...arguments for callback)
        gobject.io_add_watch(self.sockrecv, gobject.IO_IN, self._handle_incoming_data)
        # watch the ack socket for data
        gobject.io_add_watch(self.ackrecv, gobject.IO_IN, self._handle_ack)
        
        # watching for other players:
        #if(self.player == 1):
        #    gobject.timeout_add(1000, self._search_players_cb)

    def closeSockMultiRecv(self):
        # drop the membership and close the socket
        self.sockrecv.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP,
                                 socket.inet_aton(self.maddr) + socket.inet_aton(self.interface)) 
        self.sockrecv.close()

    def closeSockMultiSend(self):
        # close the send-socket 
        self.socksend.close()

    def openAckSend(self):
        self.acksend = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    def ackSend(self, data, addr):
        print 'acksend: %s --- %s'%(addr,data)
        ackaddr = ((addr, self.ackport))
        self.acksend.sendto(data, ackaddr)        
    def openAckRecv(self, addr):
        self.ackrecv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)        
        self.ackrecv.bind(addr)
        
    def _recv_cb(self, addr, data):
        # signal the message
        self.emit('recvdata', addr, data)

    def _handle_ack(self, source, condition):
        print 'handle_ack'
        # receive the ack
        data, addr = source.recvfrom(128)
        print '[ACK] %s  addr: %s '%(data, addr)
        temp = data.split(':')
        # extract number of packet, modulo 2
        selection = int(temp[1])&1
        # if name of player is not in the list for packet x:
        if not temp[0] in self.members[selection]:
            self.members[selection].append(temp[0])
        print '[ACK] %s'%self.members
        # return true otherwise the callback function gets removed
        # from the list of event sources and will not be called again        
        return True

    def _handle_incoming_data(self, source, condition):
        # receive the message
        data, addr = source.recvfrom(1024)
        print '[Recv] %s | addr: %s '%(data, addr)
        temp = data.split(':')
        # received a message - send ack
        # arg1=name of player, arg2=number of packet
        mess = '%s:%s'%(temp[1],temp[2])
        # use loopback-device if you play on one machine
        if(self.numplayers == 1):
            ipaddr = '127.0.0.1'
        else:
            ipaddr = addr[0]
        self.ackSend(mess, ipaddr)
        # if not allready received - play it
        print '[Recv]: %s'%self.playlist
        if not temp[2] in self.playlist:
            print 'Sequence: %d'%self.sequence
            self.sequence+=1
            print '[Recv] New package - play it.'
            self.playlist.append(temp[2])
            self._recv_cb(addr, data)
        else:
            print '[Recv] Received package already.'
                 
        # check if it is the first query        
        #if(temp[0] != 'Querry'):                
            # send signal/message to the gui
        # return true otherwise the callback function gets removed
        # from the list of event sources and will not be called again
        return True
    
    def _search_players_cb(self):
        if(self.notfound):
            print 'Not found all the players yet - send out a request.'
            mess = 'Querry:2:8:1'
            self.send_message(mess)
            return True
        else:
            print 'All the players found.'
            return False
        
    def send_message(self, mess):
        print '[Send] %s | addr: %s '%(mess, self.addr_port)
        self.socksend.sendto(mess, self.addr_port)
        # try in a few msec if ack's have been arrived
        gobject.timeout_add(2000, self._have_arrived_cb, mess)

    def _have_arrived_cb(self, mess):
        print '[Control] See if ack-packets have been arrived yet.'
        # get packet number 
        temp = mess.split(':')
        selection = int(temp[2])&1
        if(len(self.members[selection]) != self.numplayers):
            print '***[RETRY]------> Resend packet: %s'%temp[2]
            self.socksend.sendto(mess+':R', self.addr_port)
            return True
        else:
            print '[Control] Packet: %s arrived.'%temp[2]
            self.members[selection] = []
            return False

class LocalCommunication(gobject.GObject):
    __gsignals__ = {
        'recvdata': (gobject.SIGNAL_RUN_FIRST,
                     gobject.TYPE_NONE,
                     ([gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT]))
        }

    def __init__(self):
        gobject.GObject.__init__(self)                    
        self.sequence = 0

    def send_message(self, message):
        gobject.idle_add(self._send_message_cb, message)

    def _send_message_cb(self, message):
        self.sequence += 1
        self.emit("recvdata", None, message)
        return False
                    
class Gui:
    _GAME_TYPE_EAR = "ear"
    _GAME_TYPE_EYE = "eye"
    _GAME_TYPE_EAREYE = "eareye"

    def __init__(self, service):
        self.started = False
        self._service = service
        if self._service:
            # If we are given a service, we are _joining_ an existing game
            self.seed = service.get_published_value("seed")
            self.filename = service.get_published_value("file")
            self.maxplayers = service.get_published_value("maxplayers")
            self.player = -1
            self.game_type = service.get_published_value("type")
            # FIXME: validate game type
        else:
            # Otherwise, we are starting a brand new game
            self.seed = random.randint(0, 14567)
            self.filename = os.path.join(os.path.dirname(__file__),"alphasound.memoson")
            self.maxplayers = 4
            self.numplayers = 1
            self.player = 1
            self.game_type = self._GAME_TYPE_EAREYE

        if self._service:
            self.com = Communication('0.0.0.0', maddr, port, self.numplayers, self.player)
        else:
            self.com = LocalCommunication()
        self.com.connect('recvdata', self._handle_incoming_data_cb)
        mess = 'deci:%s:-1:%s:%s:%s'%(self.player, self._GAME_TYPE_EAREYE, self.filename, self.seed)
        self.com.send_message(mess)
        
        # connect to the csound server
        self.id = self.player
        self.csconnect()
                
        # internal globals
        self.playername = "player"+str(self.player)
        # create the list for the elements
        self.grid = []
        self.compkey = -1
        self.sound = 0
        self.pic = 0
        self.pind = 0
        self.players={'player1':0, 'player2':0, 'player3':0, 'player4':0}
        self.points = 0
        self.turn = 1
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        
        title = "Memoson - You are Player %d"%self.player
        self.window.set_title(title)
        self.window.set_border_width(10)
        self.window.connect("destroy", self.destroy)

        self.new_style = self.window.get_style().copy()
        # change the style attributes
        self.new_style.bg[gtk.STATE_NORMAL] = gtk.gdk.color_parse("white")
        # fill out the new style by attaching it to the self.window
        self.window.set_style(self.new_style)

        self.mainbox = gtk.VBox(False)
        self.row1 = gtk.HBox(False)
        self.row2 = gtk.HBox(False)
        self.row3 = gtk.HBox(False)

        # create players1
        self.frame1 = gtk.Frame("Player1: ")
        self.player1 = gtk.Label('0')
        self.player1.modify_font(pango.FontDescription("sans 10"))
        self.ebplayer1 = gtk.EventBox()
        self.ebplayer1.add(self.player1)
        self.ebplayer1.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("red"))
        self.frame1.add(self.ebplayer1)
        self.row1.pack_start(self.frame1)
        
        # create players2
        self.frame2 = gtk.Frame("Player2: ")
        self.player2 = gtk.Label('0')
        self.player2.modify_font(pango.FontDescription("sans 10"))
        self.ebplayer2 = gtk.EventBox()
        self.ebplayer2.add(self.player2)
        self.ebplayer2.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        self.frame2.add(self.ebplayer2)
        self.row1.pack_start(self.frame2)
        
        # create players3
        self.frame3 = gtk.Frame("Player3: ")
        self.player3 = gtk.Label('0')
        self.player3.modify_font(pango.FontDescription("sans 10"))
        self.ebplayer3 = gtk.EventBox()
        self.ebplayer3.add(self.player3)
        self.ebplayer3.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        self.frame3.add(self.ebplayer3)
        self.row1.pack_start(self.frame3)

        # create players4
        self.frame4 = gtk.Frame("Player4: ")
        self.player4 = gtk.Label('0')
        self.player4.modify_font(pango.FontDescription("sans 10"))
        self.ebplayer4 = gtk.EventBox()
        self.ebplayer4.add(self.player4)
        self.ebplayer4.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        self.frame4.add(self.ebplayer4)
        self.row1.pack_start(self.frame4)

        # create players5
        self.frame5 = gtk.Frame("Player5: ")
        self.player5 = gtk.Label('0')
        self.player5.modify_font(pango.FontDescription("sans 10"))
        self.ebplayer5 = gtk.EventBox()
        self.ebplayer5.add(self.player5)
        self.ebplayer5.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        self.frame5.add(self.ebplayer5)
        self.row1.pack_start(self.frame5)
        
        # create players6
        self.frame6 = gtk.Frame("Player6: ")
        self.player6 = gtk.Label('0')
        self.player6.modify_font(pango.FontDescription("sans 10"))
        self.ebplayer6 = gtk.EventBox()
        self.ebplayer6.add(self.player6)
        self.ebplayer6.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        self.frame6.add(self.ebplayer6)
        self.row1.pack_start(self.frame6)
        self.mainbox.pack_start(self.row1)

        # Console
        self.framer = gtk.Frame("Console: ")
        self.result = gtk.Label('')
        self.result.modify_font(pango.FontDescription("sans 10"))
        self.ebresult = gtk.EventBox()
        self.ebresult.add(self.result)
        self.ebresult.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        self.framer.add(self.ebresult)
        self.mainbox.pack_start(self.framer)
        
        self.separator = gtk.HSeparator()
        self.mainbox.pack_start(self.separator, False, True, 5)
                                                        
        self.mainbox.pack_start(self.row2)
        self.mainbox.pack_start(self.row3)
        self.window.add(self.mainbox)

        # Create a table for the grid dependend on the numbber oof players
        self.num_elem_x = 4
        self.num_elem_y = 4
        self.table = gtk.Table(self.num_elem_y, self.num_elem_x, True)
        self.row2.pack_start(self.table)

        # scale black
        self.scale_x = 80
        self.scale_y = 80
        self.pixbuf_i = gtk.gdk.pixbuf_new_from_file(os.path.join(os.path.dirname(__file__),"pics/black80.jpg"))
        self.scaledbuf_i = self.pixbuf_i.scale_simple(self.scale_x, self.scale_y, gtk.gdk.INTERP_BILINEAR) 
        
        # create the grid
        self.imageObj = []
        self.buttonObj = []
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
                self.buttonObj[i].connect("clicked", self.performance, i)
                self.table.attach(self.buttonObj[i], self.x, self.x+1, self.y, self.y+1)
                self.x+=1
                i+=1
            self.x=0
            self.y+=1

        self.window.show_all()        
        

    def __del__(self):        
        # close socket to csound server
        self.cssock.close()
        if self.com:
            del self.com
            self.com = None
        
    def destroy(self, widget, data=None):
        mess = "csound.SetChannel('sfplay.%d.on', 0)\n" % self.id
        self.cssock.send(mess)
        # close socket to csound server
        self.cssock.close()
        if self.com:
            del self.com
            self.com = None
        # quit the gtk-loop
        gtk.main_quit()

    def share(self, activity):
        if self.started:
            return
        self.started = True

        self._pservice = PresenceService()
        properties = {"seed": str(self.seed), "file":self.filename}
        service = self._pservice.share_activity(activity, stype="_memorygame_olpc_udp", properties=properties)
        self.com = Communication(service, self.maxplayers, self.player)
    
    def clear(self):
        self.result.set_text(str(''))
        self.ebresult.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
	return False

    def console(self, gridkey):            
        if(self.turn != self.player):
            self.result.set_text(str('Sorry, it is not your turn.'))
            self.ebresult.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("yellow"))
            gobject.timeout_add(3000, self.clear)
        elif(int(self.compkey) == gridkey):
            self.result.set_text(str('Same Item. Please choose another one.'))
            self.ebresult.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("yellow"))
            gobject.timeout_add(3000, self.clear)
        elif(self.grid[gridkey][2] == 1):
            self.result.set_text(str('Already found.'))
            self.ebresult.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("yellow"))
            gobject.timeout_add(3000, self.clear)
        else:
            # set the retry to zero
            mess = 'game:%s:%d:%d'%(self.playername, self.com.sequence, gridkey)
            self.com.send_message(mess)
            
    def performance(self, widget, num):
        self.started = True
        self.console(num)

    # connect to the csound server - open a soundfile player instrument
    def csconnect(self):
        self.cssock = socket.socket()
        self.cssock.connect(('127.0.0.1', 40002))
        mess = "csound.SetChannel('sfplay.%d.on', 1)\n" % self.id
        # start the soundfile player instrument
        self.cssock.send(mess)

    def setup_grid(self, filename, seed, numelems):
        self.pic = 1
        self.sound = 1
        self.pind = 1
        temp = []
        # set random seed
        random.seed(seed)
        # read elements from file
        fd = open(filename, 'r')
        line = fd.readline()    
        while line:
            zw = line.split()            
            zw.append('0')            
            temp.append(zw) 
            line = fd.readline()    
        fd.close()
        # select randomly numelems of the list
        self.grid = random.sample(temp, numelems)
        # make a complete copy of the list grid[:]
        # and concatenate it at the end grid.extend()
        self.grid.extend(self.grid[:])
        # shuffle th grid elements
        random.shuffle(self.grid)
        
    def _handle_incoming_data_cb(self, com, addr, temp):
        # split header from body
        mess = temp.split(':')
        if mess[0] == 'deci':
            if mess[3] == self._GAME_TYPE_EYE:
                # setup_grid(self, filename, seed, numelems):
                self.setup_grid(mess[4], mess[5], 8)
            elif mess[3] == self._GAME_TYPE_EAR:
                self.setup_grid(mess[4],mess[5], 8)
            elif mess[3] == self._GAME_TYPE_EAREYE:
                self.setup_grid(mess[4],mess[5], 8)
        elif mess[0] == 'game':
            playername = mess[1]
            gridkey = mess[3]
            compkey = self.compkey
            pind = self.pind
            grid = self.grid
            
            if(self.pic):
                self.pixbuf_p = gtk.gdk.pixbuf_new_from_file(os.path.join(os.path.dirname(__file__),grid[int(gridkey)][0]))
                self.scaledbuf_p = self.pixbuf_p.scale_simple(self.scale_x, self.scale_y, gtk.gdk.INTERP_BILINEAR) 
                self.imageObj[int(gridkey)].set_from_pixbuf(self.scaledbuf_p)
            if(self.sound):
                if not pind:
                    # make visible wich buttons have been pressed
                    self.imageObj[int(gridkey)].set_from_file(os.path.join(os.path.dirname(__file__),'pics/red80.jpg'))
                # play notes on the csound-server
                mess = "perf.InputMessage('i 102 0 3 \"%s\" %s 0.7 0.5 0')\n" % (grid[int(gridkey)][pind], self.id)
                self.cssock.send(mess)                  
            
            # if a sound/picture is open
            if(compkey != -1):
                # if the pair does not match
                if( grid[int(gridkey)][0] != grid[int(compkey)][0] ):
                    string = "self.ebplayer%d.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))"%self.turn
                    exec string
                    if(self.turn != self.numplayers):
                        self.turn+=1
                    else:
                        self.turn=1
                    string = "self.ebplayer%d.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('red'))"%self.turn
                    exec string
                    print 'turn: %d'%self.turn
                    gridkey2 = gridkey
                    compkey2 = compkey
                    gobject.timeout_add(3000, self.reset, gridkey2, compkey2)
                else:
                    # the pairs does match
                    self.result.set_text('Point for %s. One more try.'%playername)                    
                    self.ebresult.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("yellow"))
                    gobject.timeout_add(2000, self.clear)
          
                    # if you play with just sounds make pictures white
                    if not pind and not self.pic:
                        gobject.timeout_add(1000, self.set, gridkey, compkey)
                    # count the points
                    self.points+=1
                    self.players[playername]+=1
                    string = "self.%s.set_text(str(%s))"%(playername,self.players[playername])
                    exec string
                    # indicate that the matching pictures can not be pressed anymore
                    grid[int(compkey)][2] = 1;
                    grid[int(gridkey)][2] = 1;
                    # end of game
                    if(self.points == 8):
                        self.result.set_text(str('End of the game.'))
                        self.ebresult.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("yellow"))                
                self.compkey = -1
            else:        
                self.compkey = gridkey

        elif mess[0] == 'turn':
            print 'turn'
        elif mess[0] == 'mess':
            print mess[1]
        return False
    
    def reset(self, gridkey2, compkey2):
        # reset buttons if they were not matching
        self.imageObj[int(gridkey2)].set_from_file(os.path.join(os.path.dirname(__file__),'pics/black80.jpg'))
        self.imageObj[int(compkey2)].set_from_file(os.path.join(os.path.dirname(__file__),'pics/black80.jpg'))
        return False

    def set(self, gridkey, compkey):
        # make visible wich buttons have been pressed
        self.imageObj[int(gridkey)].set_from_file(os.path.join(os.path.dirname(__file__),'pics/white80.jpg'))
        self.imageObj[int(compkey)].set_from_file(os.path.join(os.path.dirname(__file__),'pics/white80.jpg'))
        return False


class MemoryActivity(Activity):
    def __init__(self, service, args):
        Activity.__init__(self, service)
        self.set_title("Memory Game")
        # setup the gui
        self.guiObject = Gui(service)        

    def share(self):
        self.guiObject.share(self)
