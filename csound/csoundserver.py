#! /usr/bin/env python

import select
import os
import logging
from threading import Thread

import csnd
from  osc.oscapi import OscApi

class CsoundServer(Thread):    
    CSOUND_PORT = 6783
    MAX_PINGS = 3
    TIMEOUT_PING = 10
    def __init__(self):
        Thread.__init__(self)
        self.oscapi = OscApi(self.CSOUND_PORT)
        self.oscapi.addmethod('/CSOUND/connect', '', self._connect)
        self.oscapi.addmethod('/CSOUND/pong', '', self._pong)
        self.oscapi.addmethod('/CSOUND/perform', 's', self._perform)
        self.oscapi.addmethod('/CSOUND/disconnect', '', self._disconnect)
        self.oscapi.addmethod('/CSOUND/quit', '', self._quit)
        self.running = 1                

        self.clients = {}
        self.start()

    def run(self):
        logging.info('start listening...')
        self.csound = csnd.Csound()
        
        while self.running:            
            inputready,outputready,exceptready = select.select([self.oscapi.iosock],[], [], self.TIMEOUT_PING)
            for s in inputready:
                if s == self.oscapi.iosock:
                    data, address = s.recvfrom(1024)
                    self.oscapi.handlemsg(data, address)
                if len(inputready) == 0:
                    self.ping()
                                
    def ping(self):
        rm = []
        for client in self.clients:
            if self.clients[client] == self.MAX_PINGS:               
                rm.append(client)
                logging.debug('[ping] remove client %s'%str(client))                
            else:
                self.oscapi.send(client, '/CSOUND/ping', [])
                self.clients[client]+=1
                ### print '     [ping] client=%s seq=%s'%(str(client), self.clients[client])

        for elem in rm:
            del self.clients[elem]
            if len(self.clients) == 0:
                self.perf.Stop()
                self.perf.Join()                                    
                self.csound.Reset()
                logging.debug('[csound] stop csound performance')                

                
    def _connect(self, *msg):            
        if msg[1] in self.clients:
            logging.debug('[connect_cb] %s already connected'%str(msg[1]))
        else:    
            self.clients[msg[1]]=0
            logging.debug('[connect_cb] %s connected'%str(msg[1]))
            if len(self.clients) == 1:
                self.perf = csnd.CsoundPerformanceThread(self.csound)
                uniorcpath = os.path.join( os.path.dirname(__file__), 'univorc.csd')
                if not os.path.exists(uniorcpath):
                    logging.error('[csound] univorc not found %s'%uniorcpath)                
                self.csound.Compile(uniorcpath)        
                self.perf.Play()
                logging.debug('[csound] start csound performance %s'%uniorcpath)


    def _disconnect(self, *msg):            
        if msg[1] not in self.clients:
            logging.debug('[disconnect_cb] %s not connected'%str(msg[1]))
        else:    
            del self.clients[msg[1]]
            logging.debug('[disconnect_cb] %s disconnected'%str(msg[1]))
            if len(self.clients) == 0:
                self.perf.Stop()
                self.perf.Join()                                    
                self.csound.Reset()
                logging.debug('[csound] stop csound performance')


    def _quit(self, *msg):
        logging.info('stop listening...')
        self.running = 0
        self.csound.Reset()
        self.csound = None
        
    
    def _pong(self, *msg):
        self.clients[msg[1]]-=1
        ### print '     [pong_cb] %s'%str(msg)


    def _perform(self, *msg):
        logging.debug('     [perform_cb] %s'%str(msg[0][2]))
        self.perf.InputMessage(msg[0][2])


