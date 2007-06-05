""" This file is based on simpleOSC 0.2 by Daniel Holth.
This file has been modified by Simon Schampijer.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""


import socket
import errno
import logging
import sys

import osccore


class OscApi(object):
    def __init__(self, port=None, host=None):
        """create the send/receive socket and the callback manager
        bind the socket to a name (host and port) 

        Keyword arguments:
        port -- the port
                if no port is specified the socket will not be bound to an address and
                will only be used for sending
        host -- the host address, can be a dotted decimal address (e.g. '192.168.0.100')
                or a hostname (e.g. 'machine', 'localhost') 
                if you do not specify a hostname the socket will listen on all the
                devices for incoming messages        
        """
        
        self.manager = 0
        self.iosock = 0
        self.iosock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.manager = osccore.CallbackManager()

        self.isserver = 0
        
        if port is not None:
            if host is None:
                host = ""        
            try:        
                self.iosock.bind((host, port))
                self.isserver = 1        
            except socket.error:             
                if errno.EADDRINUSE:
                    logging.error("Port " +str(port)+ " in use." +
                                  " Maybe another oscapi is still or already running?" +
                                  " oscapi can only be used for sending.")
                    self.iosock.close()
                    self.iosock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.iosock.setblocking(0) 


    def addmethod(self, path, types, func):
        '''adds an osc method to the listener

        Keyword arguments:
        func -- the callback function which gets called when the appropriate osc message is received
        path -- the path (identifier) of the osc message
        
        '''        
        self.manager.add(func, path, types)


    def handlemsg(self, data, addr):
        '''give the information read from the socket to the osc message dispatcher

        Keyword arguments:
        data -- the data read from the socket
        addr -- address the message is received from        
        '''
        self.manager.handle(data, addr)     


    def _create_binarymsg(self, path, data):
        """create an OSC message in binary format 

        Keyword arguments:
        path -- the path (identifier) of the osc message
        data -- the data of the message

        return: the osc message in binary format
        """
        m = osccore.OSCMessage()
        m.setAddress(path)

        if len(data) != 0:
            for x in data:  
                m.append(x)

        return m.getBinary()


    def send(self, to, path, data):
        """send an osc message to the address specified
        
        Keyword arguments:
        to -- address of receiver in the form (ipaddr, bundle)
        path -- the path of the osc message
        data -- the data of the message
        """        
        ### resolve host? [a,b,host] = socket.gethostbyaddr(to[0])
        msg = self._create_binarymsg(path, data)
        try:        
            self.iosock.sendto(msg, (to[0],to[1]))         
        except socket.error:
            cla, exc, trbk = sys.exc_info()
            try:
                excArgs = exc.__dict__["args"]
            except KeyError:
                excArgs = "<no args>"
            logging.error('error '+str(excArgs))

    def createbundle(self):
        """create the header of a bundle of OSC messages"""
        b = osccore.OSCMessage()
        b.setAddress("")
        b.append("#bundle")
        b.append(0)
        b.append(0)
        return b

    def appendbundle(self, bundle, path, data):
        """append osc message to the bundle
        
        Keyword arguments:
        bundle -- the bundle to which you want to append a message
        path -- the path of the OSC message
        data -- the data of the message
        """
        msg = self._create_binarymsg(path, data)
        bundle.append(msg, 'b')


    def sendbundle(self, to, bundle):
        """send bundle to the address specified
        
        Keyword arguments:
        to -- address of receiver in the form (ipaddr, bundle)
        bundle -- the bundle to send
        """
        try:
            self.iosock.sendto(bundle.message, to)
        except socket.error:
            cla, exc, trbk = sys.exc_info()
            try:
                excArgs = exc.__dict__["args"]
            except KeyError:
                excArgs = "<no args>"
            logging.error('error '+str(excArgs))

