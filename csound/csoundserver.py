#    Copyright (C) 2006, 2007, 2008 One Laptop Per Child
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
            if self.csound.Compile(uniorcpath) == -1:
                _logger.debug('error compiling csound orchestra %s'%uniorcpath)
                return 1
            self.perf.Play()
            return 0
        
    def pause(self):            
        self.perf.Stop()
        self.perf.Join()                                    
        self.csound.Reset()
        _logger.debug('stop performance')

    def perform(self, msg):
        _logger.debug('     [perform_cb] %s'%str(msg))
        self.perf.InputMessage(str(msg))

    def quit(self):
        _logger.info('quit')
        self.perf.Stop()
        self.perf.Join()                                    
        self.csound.Reset()
        self.csound = None            


