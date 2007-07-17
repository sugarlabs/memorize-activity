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

_logger = logging.getLogger('model')

class Pair(gobject.GObject):    
    __gproperties__ = {
        'aimg'    : (str, None, None, None, gobject.PARAM_READWRITE),
        'asnd'    : (str, None, None, None, gobject.PARAM_READWRITE),
        'achar'    : (str, None, None, None, gobject.PARAM_READWRITE),
        'acharalign' : (str, None, None, None, gobject.PARAM_READWRITE),
        'bimg'    : (str, None, None, None, gobject.PARAM_READWRITE),        
        'bsnd'    : (str, None, None, None, gobject.PARAM_READWRITE),
        'bchar'    : (str, None, None, None, gobject.PARAM_READWRITE),
        'bcharalign': (str, None, None, None, gobject.PARAM_READWRITE),
        'color': (gobject.TYPE_INT, 'Base', 'Base', 0, 10, 0, gobject.PARAM_READWRITE)
    }
        
    def __init__(self):
        gobject.GObject.__init__(self)        
        self._properties = {'aimg':None, 'asnd':None, 'achar':None, 'acharalign':'1', 'bimg':None, 
                            'bsnd':None, 'bchar':None, 'bcharalign':1, 'color':100}                
        
    def do_get_property(self, pspec):
        """Retrieve a particular property from our property dictionary 
        """
        if pspec.name == "aimg":
            return self._properties["aimg"]
        elif pspec.name == "asnd":
            return self._properties["asnd"]
        elif pspec.name == "achar":
            return self._properties["achar"]
        elif pspec.name == "acharalign":
            return self._properties["acharalign"]
        elif pspec.name == "bimg":
            return self._properties["bimg"]
        elif pspec.name == "bsnd":
            return self._properties["bsnd"]
        elif pspec.name == "bchar":
            return self._properties["bchar"]
        elif pspec.name == "bcharalign":
            return self._properties["bcharalign"]
        elif pspec.name == "color":
            return self._properties["color"]

    def set_property(self, name, value):
        if name == 'aimg':
            self._properties['aimg'] = value
        elif name == "asnd":
            self._properties["asnd"] = value
        elif name == "achar":
            self._properties["achar"] = value
        elif name == "acharalign":
            self._properties["acharalign"] = int(value)
        elif name == "bimg":
            self._properties["bimg"] = value
        elif name == "bsnd":
            self._properties["bsnd"] = value
        elif name == "bchar":
            self._properties["bchar"] = value
        elif name == "bcharalign":
            self._properties["bcharalign"] = value
        elif name == "color":
            self._properties["color"] = value


class Model(object):
    ''' The model of the activity. Contains methods to read and save
    the configuration for a game from xml. Stores the pairs and grid
    information.    
    '''
    _GAMES_PATH = os.path.join(os.path.dirname(__file__), 'games')
    
    def __init__(self, dtdpath):
        self.data = {}
        self.dtdpath = dtdpath
        self.data['face'] = ''
        
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

    def read(self, gamename):
        ''' reades the configuration from an xml file '''
        self.data['path'] = os.path.join( self._GAMES_PATH, gamename)
        self.data['pathimg'] = os.path.join(self.data['path'], 'images')
        self.data['pathsnd'] = os.path.join(self.data['path'], 'sounds')
        self.pairs = {}

        try:
            doc = libxml2.parseFile(os.path.join(self.data['path'], gamename+'.mem'))            
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
                        self.pairs[str(self.idpair)] = pair
                        self.idpair+=1                        
                    elif( elem.name == 'memorize' ):
                        for attribute in attributes:
                            if(attribute.name == 'text'):
                                pass
                            elif(attribute.name == 'name'):                            
                                self.data['name'] = attribute.content
                            elif(attribute.name == 'scoresnd'):                            
                                self.data['scoresnd'] = attribute.content            
                            elif(attribute.name == 'winsnd'):                            
                                self.data['winsnd'] = attribute.content            
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
                _logger.error('Read: Error in validation of the file')
                doc.freeDoc()
                return 1
            doc.freeDoc()
            return 0
        except libxml2.parserError, e:
            _logger.error('Read: Error parsing file ' +str(e))
            return 2
            
    def save(self, filename):
        ''' saves the configuration to an xml file '''
        doc = libxml2.newDoc("1.0")
        root = doc.newChild(None, "memorize", None)
        
        if(self.data.get('name', None) != None):                            
            root.setProp("name", self.data['name'])
        else:
            _logger.error('Save: No name is specified. Can not save game.')
            return 1
        if(self.data.get('scoresnd', None) != None):                            
            root.setProp("scoresnd", self.data['scoresnd'])
        if(self.data.get('winsnd', None) != None):                            
            root.setProp("winsnd", self.data['winsnd'])
        if(self.data.get('divided', None) != None):                            
            root.setProp("divided", self.data['divided'])
        if(self.data.get('face', None) != None):                            
            root.setProp("face", self.data['face'])
        if(self.data.get('face1', None) != None):                            
            root.setProp("face1", self.data['face1'])
        if(self.data.get('face2', None) != None):                            
            root.setProp("face2", self.data['face2'])
                                
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
            # elem.setProp("color", str(self.pairs[key].props.color))
        
        if doc.validateDtd(self.ctxt, self.dtd):
            doc.saveFormatFile(filename, 1)
        else:
            _logger.error('Save: Error in validation of the file')
            doc.freeDoc()
            return 2
        doc.freeDoc()
        return 0


    def def_grid(self, size):
        ''' create the grid for the play from the pairs information
        and shuffles the grid so they always appear in a different
        place        
        '''
        psize=(size*size/2)
        _logger.debug('Size requested: %d' %psize)
        self.grid = []
        temp1 = []
        temp2 = []
        i=0

        # shuffle the pairs first to avoid only taking the first ones when there are more
        # pairs in the config file then the grid is using
        keys = model.pairs.keys()
        random.shuffle(keys)

        for key in keys:
            if i < psize:
                elem = {}
                elem['pairkey'] = key
                elem['state'] = '0'
                elem['ab'] = 'a'
                elem['charalign'] = '0'
                if self.pairs[key].props.aimg != None:
                    elem['img'] = os.path.join(self.data['pathimg'], self.pairs[key].props.aimg)
                if self.pairs[key].props.asnd != None:
                    if os.path.isfile(os.path.join(self.data['pathsnd'], self.pairs[key].props.asnd)):
                        elem['snd'] = os.path.join(self.data['pathsnd'], self.pairs[key].props.asnd)
                if self.pairs[key].props.achar != None:
                    elem['char'] = self.pairs[key].props.achar
                    elem['charalign'] = self.pairs[key].props.acharalign                    
                temp1.append(elem)
                
                elem = {}
                elem['pairkey'] = key
                elem['state'] = '0'
                elem['ab'] = 'b'
                elem['charalign'] = '0'
                if self.pairs[key].props.bimg != None:
                    elem['img'] = os.path.join(self.data['pathimg'], self.pairs[key].props.bimg)
                if self.pairs[key].props.bsnd != None:
                    if os.path.isfile(os.path.join(self.data['pathsnd'], self.pairs[key].props.bsnd)):
                        elem['snd'] = os.path.join(self.data['pathsnd'], self.pairs[key].props.bsnd)
                if self.pairs[key].props.bchar != None:
                    elem['char'] = self.pairs[key].props.bchar
                    elem['charalign'] = self.pairs[key].props.bcharalign
                temp2.append(elem)    
                i+=1
            else:
                break
        
        numpairs = len(self.pairs)      
        if numpairs < psize:
            _logger.debug('Defgrid: We did not have enough pairs. requested=%s had=%s' %(psize, numpairs))
        self.data['size'] = str(size)

        if self.data['divided'] == '1':
            random.shuffle(temp1)
            random.shuffle(temp2)
            temp1.extend(temp2)
        else:
            temp1.extend(temp2)
            random.shuffle(temp1)
        self.grid = temp1
        _logger.debug('Defgrid: grid( size=%s ): %s' %(self.data['size'], self.grid))

    

if __name__ == '__main__':
    model = Model(os.path.dirname(__file__))
    model.read('numbers')

    model.def_grid(8)
    print 'grid %s'%model.grid 

    model.save('/tmp/save.mem')
    
    '''
    print 'name=%s scoresnd=%s winsnd=%s div=%s' %(model.data['name'], model.data['scoresnd'],
                                                   model.data['winsnd'], model.data['divided'])

    model.def_grid(4)
    print 'grid %s'%model.grid #['size']

    print 'Test set state of tile 7:'
    tilenum = 7
    model.grid[tilenum]['state'] = '1'   
    print '   %s' %model.grid[tilenum]

    print 'Test sound:'    
    snd = model.grid[tilenum].get('snd', None)
    if snd == None:
        print '   no sound'
    else:
        print '   play sound=%s'%snd

    print 'Test the same function: 0 1'
    if model.grid[0]['pairkey'] == model.grid[1]['pairkey']:
        print '   they are the same'
    else:
       print '   they are NOT the same'

    for tile in model.grid:
        id = model.grid.index(tile)
        if tile.get('img', None):
            print 'we got an image=%s '%tile['img']
        elif tile.get('char', None):
            print 'we got an char=%s'%tile.get('char')
        else:
            print 'we got no pic so prepare for sound game'
            
    print '\n_______________________________\n'
    
    if model.read('addition') == 0:
        print '%s' %model.pairs[0]._properties
        print 'name=%s' %model.data['name']
        print 'scoresnd=%s' %model.data['scoresnd']
        print 'winsnd=%s' %model.data['winsnd']
        print 'div=%d' %model.data['divided']
    
        model.def_grid(12)
        for tile in model.grid:
            id = model.grid.index(tile)
            if tile.get('img', None):
                print 'we got an image=%s '%tile.get('img')
            elif tile.get('char', None):
                print 'we got an char=%s'%tile.get('char')
            else:
                print 'we got no img so prepare for sound game'

    else:   
        print 'error during reading of the game'


    print '\n_______________________________\n'    
    if model.read('numbers') == 0:
        print '%s' %model.pairs[0]._properties
        print 'name=%s' %model.data['name']
        print 'scoresnd=%s' %model.data['scoresnd']
        print 'winsnd=%s' %model.data['winsnd']
        print 'div=%d' %model.data['divided']
        print 'face1=%s' %model.data['face1']
        print 'face2=%s' %model.data['face2']
    
        model.def_grid(12)
        for tile in model.grid:
            id = model.grid.index(tile)
            if tile.get('img', None):
                print 'we got an image=%s '%tile.get('img')
            elif tile.get('char', None):
                print 'we got an char=%s'%tile.get('char')
            else:
                print 'we got no img so prepare for sound game'

    else:   
        print 'error during reading of the game'
    '''
