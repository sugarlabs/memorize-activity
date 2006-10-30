#!/usr/bin/python
import select
import sys
import socket
import threading
import time
import os.path
import csnd

# this is a multiple-client csound server
# the listener is put in a separate thread

class CsoundServerMult:
    # server start-up
    def __init__(self, addr):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.size = 1024
        print "*** CsServer: Csound Python server listening at: @%s:%d" % (ipaddr, port)
        self.server.listen(32)
        self.input = [self.server,sys.stdin]
        self.running = 1

    # this is the interpreter function
    # if something is seen on the socket
    # it executes it as Python code
    def interpret(self):
        # run the universal orchestra        
        csound = csnd.Csound()
        perf = csnd.CsoundPerformanceThread(csound)
        csound.Compile(os.path.join(_DIR_CSSERVER, 'univorc.csd'))
        perf.Play()
        
        while self.running:
            inputready,outputready,exceptready = select.select(self.input,[],[])

            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print'*** CsServer: Client has been accepted on: ',address
                    self.input.append(client)

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    csound.SetChannel('udprecv.0.on', 0)
                    perf.Stop()
                    perf.Join()                                    
                    csound.Reset()
                    csound = None
                    print '*** CsServer: The csound instance has been reset successfully.'
                    self.running = 0 
              
                else:
                    # handle all other sockets
                    data = s.recv(self.size)
                    print data
                    if data.strip('\n') == 'off()':
                        csound.SetChannel('udprecv.0.on', 0)
                        perf.Stop()
                        perf.Join()                                    
                        csound.Reset()
                        csound = None
                        print '*** CsServer: The csound instance has been reset successfully.'
                        self.running = 0 
        
                    elif data:
                        try:
                            exec data
                        except:
                            print "exception in code: " + data
                    else:
                        print '*** CsServer: remove socket: ', s.fileno()
                        s.close()
                        self.input.remove(s)

        for i in self.input:
            i.close()
            self.input.remove(i)
        self.server.close()
        print '*** CsServer: The server has been closed.'
        
if __name__=="__main__":
    if len(sys.argv) > 1:
        ipaddr = sys.argv[1]
    else:
        ipaddr = 'localhost'
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = 40002

    _DIR_CSSERVER =  os.path.join(os.path.dirname(__file__))
    s = CsoundServerMult((ipaddr, port))
    s.interpret()
    
