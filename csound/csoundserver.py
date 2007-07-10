#! /usr/bin/env python

import os
import logging
from threading import Thread

import csnd

_logger = logging.getLogger('csound')

class CsoundServer(Thread):    
    def __init__(self):
        Thread.__init__(self)
        self.csound = csnd.Csound()

    def start(self):            
        self.perf = csnd.CsoundPerformanceThread(self.csound)
        uniorcpath = os.path.join( os.path.dirname(__file__), 'univorc.csd')
        if not os.path.exists(uniorcpath):
            _logger.error('univorc not found %s'%uniorcpath)
        else:
            self.csound.Compile(uniorcpath)        
            self.perf.Play()
            _logger.debug('start csound performance %s'%uniorcpath)

    def pause(self):            
        self.perf.Stop()
        self.perf.Join()                                    
        self.csound.Reset()
        _logger.debug('stop performance')

    def perform(self, msg):
        _logger.debug('     [perform_cb] %s'%str(msg))
        self.perf.InputMessage(msg)

    def quit(self):
        _logger.info('quit')
        self.perf.Stop()
        self.perf.Join()                                    
        self.csound.Reset()
        self.csound = None            


