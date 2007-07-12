#! /usr/bin/env python
#
#    Copyright (C) 2006, 2007, One Laptop Per Child
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

import libxml2
import os
import logging
import random
import gobject

IMAGES_PATH = 'games/drumgit/images'
SOUNDS_PATH = 'games/drumgit/sounds'
GAME_PATH = ''

_logger = logging.getLogger('model')


class Pair(gobject.GObject):    
    __gproperties__ = {
        'aimg'    : (str, None, None, None, gobject.PARAM_READWRITE),
        'asnd'    : (str, None, None, None, gobject.PARAM_READWRITE),
        'achar'    : (str, None, None, None, gobject.PARAM_READWRITE),
        'bimg'    : (str, None, None, None, gobject.PARAM_READWRITE),        
        'bsnd'    : (str, None, None, None, gobject.PARAM_READWRITE),
        'bchar'    : (str, None, None, None, gobject.PARAM_READWRITE),
        'color': (gobject.TYPE_INT, 'Base', 'Base', 0, 10, 0, gobject.PARAM_READWRITE)
    }
        
    def __init__(self):
        gobject.GObject.__init__(self)        
        self._properties = {'aimg':None, 'asnd':None, 'bimg':None, 'bsnd':None, 'color':100}                
        
    def do_get_property(self, pspec):
        """Retrieve a particular property from our property dictionary 
        """
        if pspec.name == "aimg":
            return self._properties["aimg"]
        elif pspec.name == "asnd":
            return self._properties["asnd"]
        elif pspec.name == "achar":
            return self._properties["achar"]
        elif pspec.name == "bimg":
            return self._properties["bimg"]
        elif pspec.name == "bsnd":
            return self._properties["bsnd"]
        elif pspec.name == "bchar":
            return self._properties["bchar"]
        elif pspec.name == "color":
            return self._properties["color"]

    def set_property(self, name, value):
        if name == 'aimg':
            self._properties['aimg'] = value
        elif name == "asnd":
            self._properties["asnd"] = value
        elif name == "achar":
            self._properties["achar"] = value
        elif name == "bimg":
            self._properties["bimg"] = value
        elif name == "bsnd":
            self._properties["bsnd"] = value
        elif name == "bchar":
            self._properties["bchar"] = value
        elif name == "color":
            self._properties["color"] = int(value)
    '''        
    def do_set_property(self, props, value):
        if props.name == 'a_img':
            self._properties['a_img'] = value
    '''

class Model(object):
    ''' The model of the activity. Contains methods to read and save
    the configuration for a game from xml. Stores the pairs and grid
    information.    
    '''    
    def __init__(self, gamepath, dtdpath, name='noname'):
        self.data = {}
        self.gamepath = gamepath
        self.dtdpath = dtdpath

        try:
            self.dtd = libxml2.parseDTD(None, os.path.join(self.dtdpath, 'memorize.dtd'))
        except libxml2.parserError, e:
            _logger.error('No memorize.dtd found ' +str(e))
            self.dtd = None
        self.ctxt = libxml2.newValidCtxt()               

        self.pairs = {}
        self.grid = []

        # used by the leader of the game to keep track of the game state
        self.players = {}
        self.player_active = 0
        self.selected = 0
        self.turn = 0
        self.started = 0
        self.count = 0

    def read(self, filename):
        ''' reades the configuration from an xml file '''
        try:
            doc = libxml2.parseFile(os.path.join(self.gamepath, filename))            
            if doc.validateDtd(self.ctxt, self.dtd):
        
                # get the requested nodes
                xpa = doc.xpathNewContext()
                res = xpa.xpathEval("//*")

                # write their content to the data structure
                self.idpair = 0
                for elem in res:
                    attributes = elem.get_properties()
                    pair = Pair()
                    if( elem.name == 'pair' ):
                        for attribute in attributes:
                            if(attribute.name == 'text'):
                                pass
                            else:                            
                                pair.set_property(attribute.name, attribute.content)
                        self.pairs[self.idpair] = pair
                        self.idpair+=1                        
                    elif( elem.name == 'memorize' ):
                        for attribute in attributes:
                            if(attribute.name == 'text'):
                                pass
                            elif(attribute.name == 'name'):                            
                                self.data['game_name'] = attribute.content            
                            elif(attribute.name == 'scoresnd'):                            
                                self.data['scoresnd'] = attribute.content            
                            elif(attribute.name == 'winsnd'):                            
                                self.data['winsnd'] = attribute.content            
                            elif(attribute.name == 'divided'):                            
                                self.data['divided'] = attribute.content
                            elif(attribute.name == 'divided'):                            
                                self.data['divided'] = attribute.content
                            elif(attribute.name == 'face'):                            
                                self.data['face'] = attribute.content
                            elif(attribute.name == 'face1'):                            
                                self.data['face1'] = attribute.content
                            elif(attribute.name == 'face2'):                            
                                self.data['face2'] = attribute.content                                
                xpa.xpathFreeContext()
            else:
                _logger.error('Error in validation of the file')
            doc.freeDoc()
        except libxml2.parserError, e:
            _logger.error('Error parsing file ' +str(e))

            
    def save(self, filename):
        ''' saves the configuration to an xml file '''
        doc = libxml2.newDoc("1.0")
        root = doc.newChild(None, "memorize", None)
        root.setProp("name", self.data['game_name'])
        ### Fixme: add other attributes here
        for key in self.pairs:
            
            elem = root.newChild(None, "pair", None)
            if self.pairs[key].props.aimg != None:
                elem.setProp("aimg", self.pairs[key].props.aimg)
            if self.pairs[key].props.asnd != None:
                elem.setProp("asnd", self.pairs[key].props.asnd)
            if self.pairs[key].props.achar != None:
                elem.setProp("achar", self.pairs[key].props.achar)
            if self.pairs[key].props.bimg != None:
                elem.setProp("bimg", self.pairs[key].props.bimg)
            if self.pairs[key].props.bsnd != None:
                elem.setProp("bsnd", self.pairs[key].props.bsnd)
            if self.pairs[key].props.bchar != None:
                elem.setProp("bchar", self.pairs[key].props.bchar)
            elem.setProp("color", str(self.pairs[key].props.color))
        
        if doc.validateDtd(self.ctxt, self.dtd):
            doc.saveFormatFile(filename, 1)
        doc.freeDoc()    


    def def_grid(self, size):
        ''' create the grid for the play from the pairs information
        and shuffles the grid so they always appear in a different
        place
        grid [pair_key, a_or_b, flipstatus]
        '''
        _logger.debug(' pairs: %s', self.pairs)
        i=0
        for key in self.pairs.iterkeys():
            if i < size:
                self.grid.append([key, 0, 0])
                self.grid.append([key, 1, 0])
                i+=1
            else:
                break

        numpairs = len(self.pairs)      
        if numpairs < size:
            _logger.debug('We did not have enough pairs. requested=%s had=%s' %(numpairs, size))

        self.data['size'] = numpairs
        
        random.shuffle(self.grid)
        _logger.debug(' grid: %s', self.grid)


    def gettile(self, tilenum):
        ''' gets the information of an object associated with a tile number '''
        img = None
        snd = None
        char = None
        pairkey, moch, state = self.grid[tilenum]                
        if moch == 0:
            if self.pairs[pairkey].props.aimg != None:                    
                img = os.path.join(IMAGES_PATH, self.pairs[pairkey].props.aimg)
            if self.pairs[pairkey].props.asnd != None:                    
                snd = os.path.join(SOUNDS_PATH, self.pairs[pairkey].props.asnd)
            char = self.pairs[pairkey].props.achar
        if moch == 1:
            if self.pairs[pairkey].props.bimg != None:                    
                img = os.path.join(IMAGES_PATH, self.pairs[pairkey].props.bimg)
            if self.pairs[pairkey].props.bsnd != None:                    
                snd = os.path.join(SOUNDS_PATH, self.pairs[pairkey].props.bsnd)
            char = self.pairs[pairkey].props.bchar
        color = self.pairs[pairkey].props.color
        return (img, snd, char, color)


    def same(self, a, b):
        ''' checks wether two tiles are matching '''
        pairkeya, moch, state = self.grid[a]
        pairkeyb, moch, state = self.grid[b]
        return (pairkeya == pairkeyb)


    

if __name__ == '__main__':
    model = Model(GAME_PATH, os.path.dirname(__file__))
    model.read('drumgit.mem')
    print '%s' %model.pairs[0]._properties
    print 'name=%s' %model.data['game_name']
    print 'scoresnd=%s' %model.data['scoresnd']
    print 'winsnd=%s' %model.data['winsnd']
    print 'div=%s' %model.data['divided']
    model.def_grid(8)
    print 'grid size=%d'%model.data['size']
    print model.grid

    i=0
    while i < model.data['size']:
        pairkey, moch, state = model.grid[i]                
        if moch == 0:
            if model.pairs[pairkey].props.aimg != None:                    
                print model.pairs[pairkey].props.aimg
        if moch == 1:
            if model.pairs[pairkey].props.bimg != None:                    
                print model.pairs[pairkey].props.bimg
        i+=1

        
    '''    
    print '\n_______________________________\n'
    
    model.read('addition.mem')
    print '%s' %model.pairs[0]._properties
    print 'name=%s' %model.data['game_name']
    print 'scoresnd=%s' %model.data['scoresnd']
    print 'winsnd=%s' %model.data['winsnd']
    print 'div=%s' %model.data['divided']
    
    model.def_grid(12)
    print model.grid
    print model.gettile(0)
    print model.gettile(1)
    model.save('/tmp/mod.txt')
    '''
