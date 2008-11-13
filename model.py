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

import libxml2
from os import environ, makedirs, chmod
from os.path import join, basename, dirname, isdir, split, normpath
import logging
import random
import gobject
import zipfile
import tempfile
from sugar import profile
from sugar.datastore import datastore

_logger = logging.getLogger('model')

class Pair(gobject.GObject):    
    __gproperties__ = {
        'aimg' : (str, None, None, None, gobject.PARAM_READWRITE), 
        'asnd' : (str, None, None, None, gobject.PARAM_READWRITE), 
        'achar': (str, None, None, None, gobject.PARAM_READWRITE), 
        'bimg' : (str, None, None, None, gobject.PARAM_READWRITE), 
        'bsnd' : (str, None, None, None, gobject.PARAM_READWRITE), 
        'bchar': (str, None, None, None, gobject.PARAM_READWRITE), 
        'color': (gobject.TYPE_INT, 'Base', 'Base', 0, 10, 0, gobject.PARAM_READWRITE)
    }
        
    def __init__(self):
        gobject.GObject.__init__(self)        
        self._properties = {'aimg':None, 'asnd':None, 'achar':None, 'bimg':None, 
                            'bsnd':None, 'bchar':None, 'color':100}                
        
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
            self._properties["color"] = value


class Model(object):
    ''' The model of the activity. Contains methods to read and write
    the configuration for a game from xml. Stores the pairs and grid
    information.    
    '''
    
    def __init__(self, game_path, dtd_path = None):
        self.data = {}
        if dtd_path == None:
            self.dtd_path = dirname(__file__)
        else:
            self.dtd_path = dtd_path
            
        if isdir(game_path):
            self.game_path = game_path
        else:
            _logger.error('Game_path not found ' +str(e))
            return
            
        self.data['face'] = ''
        self.data['align'] = '1'
        
        try:
            self.dtd = libxml2.parseDTD(None, join(self.dtd_path, 'memorize.dtd'))
        except libxml2.parserError, e:
            _logger.error('Init: no memorize.dtd found ' +str(e))
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

    def read(self, game_file):
        tmp_root = join(environ['SUGAR_ACTIVITY_ROOT'], 'instance')
        temp_folder = tempfile.mkdtemp(dir=tmp_root)
        chmod(temp_folder,0777)
        self.data['key'] = basename(game_file)
        self.data['game_file'] = game_file
        self.data['path'] = temp_folder
        self.data['pathimg'] = join(self.data['path'], 'images')
        self.data['pathsnd'] = join(self.data['path'], 'sounds')
        
        ''' extracts files in the zip file '''
        game_name = basename(game_file)[:-4]
        zipFile = zipfile.ZipFile(game_file, "r")
        for each in zipFile.namelist():
            if not each.endswith('/'):
                root, name = split(each)
                directory = normpath(join(self.data['path'], root))
                if not isdir(directory):
                    makedirs(directory)
                file(join(directory, name), 'wb').write(zipFile.read(each))

        self.pairs = {}
        
        ''' reads the configuration from an xml file '''
        try:
            xml_file = join(environ['SUGAR_ACTIVITY_ROOT'], self.data['path'], 'game.xml')
            doc = libxml2.parseFile(xml_file)
            if doc.validateDtd(self.ctxt, self.dtd):
        
                # get the requested nodes
                xpa = doc.xpathNewContext()
                res = xpa.xpathEval("//*")

                # write their content to the data structure
                self.idpair = 0
                for elem in res:
                    attributes = elem.get_properties()
                    pair = Pair()
                    if(elem.name == 'pair'):
                        for attribute in attributes:
                            if(attribute.name == 'text'):
                                pass
                            else:                            
                                pair.set_property(attribute.name, attribute.content)
                        self.pairs[str(self.idpair)] = pair
                        self.idpair+=1                        
                    elif(elem.name == 'memorize'):
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
                            elif(attribute.name == 'align'):                            
                                self.data['align'] = attribute.content
                            elif(attribute.name == 'equal_pairs'):                            
                                self.data['equal_pairs'] = attribute.content    
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
        
    def write(self, equal_pairs, divided):
        ''' writes the configuration to an xml file '''
        doc = libxml2.newDoc("1.0")
        root = doc.newChild(None, "memorize", None)
        
        if(self.data.get('name', None) != None):                            
            root.setProp("name", self.data['name'])
        
        if divided:
            root.setProp('divided', '1')
            root.setProp('face1', '1')
            root.setProp('face2', '2')
        else:
            root.setProp('divided', '0')
        
        if equal_pairs:
            root.setProp('equal_pairs', str(equal_pairs))
        
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
        if(self.data.get('align', None) != None):                            
            root.setProp("align", self.data['align'])

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
            doc.saveFormatFile(join(self.game_path, 'game.xml'), 1)
        else:
            _logger.error('Write: Error in validation of the file')
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
        keys = self.pairs.keys()
        random.shuffle(keys)

        for key in keys:
            if i < psize:
                elem = {}
                elem['pairkey'] = key
                elem['state'] = '0'
                elem['ab'] = 'a'
                if self.pairs[key].props.aimg != None:
                    elem['img'] = self.pairs[key].props.aimg
                if self.pairs[key].props.asnd != None:
                    elem['snd'] = self.pairs[key].props.asnd
                if self.pairs[key].props.achar != None:
                    elem['char'] = self.pairs[key].props.achar
                temp1.append(elem)
                
                elem = {}
                elem['pairkey'] = key
                elem['state'] = '0'
                elem['ab'] = 'b'
                if self.pairs[key].props.bimg != None:
                    elem['img'] = self.pairs[key].props.bimg
                if self.pairs[key].props.bsnd != None:
                    elem['snd'] = self.pairs[key].props.bsnd
                if self.pairs[key].props.bchar != None:
                    elem['char'] = self.pairs[key].props.bchar
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
        _logger.debug('Defgrid: data: %s' %self.data)

    def set_data_grid(self, data, grid):
        self.data = data
        self.grid = grid
        
    def save_byte_array(self, path, title= None, color= None):
        if color == None:
            color = profile.get_color().to_string()
        _logger.debug('Save new game in datastore')

        # Saves the zip in datastore
        gameObject = datastore.create()
        gameObject.metadata['title'] = title
        gameObject.metadata['mime_type'] = 'application/x-memorize-project'
        gameObject.metadata['icon-color'] = color
        gameObject.file_path = path
        datastore.write(gameObject)      
                
