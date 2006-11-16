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

import OSC
import socket
import errno

class OscApi:
    def __init__(self):
       """ inits manager and outsocket
       """
       # globals
       self.addressManager = 0
       self.ioSocket = 0
       self.ioSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       self.addressManager = OSC.CallbackManager()

    def createListener(self, ipAddr, port):
        """create and return an inbound socket
        """
        i=0
        while i < 10:
            try:
                self.ioSocket.bind(('127.0.0.1', port))
                #logging.debug(" Memosono-Server has port "+str(self.port) )
                i = 10
            except socket.error:             
                if errno.EADDRINUSE:
                    #logging.debug(" Port in use. Try another one. "+str(port))
                    port+=1
                    i+=1
                    if i is 10:
                        #logging.debug(" No free port found. Memosono will NOT work.")
                        self.ioSocket.bind((ipAddr, port))

        self.ioSocket.setblocking(0) # if not waits for msgs to arrive blocking other events                        
        return (self.ioSocket, port)

    def bind(self, func, oscaddress):
        """ bind certains oscaddresses with certain functions in address manager
        """
        self.addressManager.add(func, oscaddress)

    def recvhandler(self, data, addr):
        self.addressManager.handle(data, addr)     


#############----send----####################

    def createBinaryMsg(self, oscAddress, dataArray):
        """create and return general type binary OSC msg"""
        m = OSC.OSCMessage()
        m.setAddress(oscAddress)

        if len(dataArray) != 0:
            for x in dataArray:  ## append each item of the array to the message
                m.append(x)

        return m.getBinary() # get the actual OSC to send

    def sendOSC(self, stufftosend, ipAddr, port): # outSocket, 
        """ send OSC msg or bundle as binary"""
        self.ioSocket.sendto(stufftosend, (ipAddr, port))


############################### send message

    def sendMsg(self, oscAddress, dataArray, ipAddr, port):#, outSocket):
        """create and send normal OSC msgs"""
        msg = self.createBinaryMsg(oscAddress, dataArray)
        self.sendOSC(msg, ipAddr, port)  # outSocket, 

############################### bundle stuff + send bundle
    def createBundle(self):
        """create bundled type of OSC messages"""
        b = OSC.OSCMessage()
        b.setAddress("")
        b.append("#bundle")
        b.append(0)
        b.append(0)
        return b

    def appendToBundle(self, bundle, oscAddress, dataArray):
        """create OSC mesage and append it to a given bundle"""
        OSCmsg = self.createBinaryMsg(oscAddress, dataArray)
        bundle.append(OSCmsg, 'b')

    def sendBundle(self, bundle, ipAddr, port):#, outSocket):
        """convert bundle to a binary and send it"""
        self.sendOSC(bundle.message, ipAddr, port) # outSocket

