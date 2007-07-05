import libxml2
import os
import logging
import random

IMAGES_PATH = 'games/drumgit/images'

_logger = logging.getLogger('model')

class Model(object):
    ''' The model of the activity. Contains methods to read and save
    the configuration for a game from xml. Stores the pairs and grid
    information.    
    '''    
    def __init__(self, gamepath, dtdpath, name='noname'):
        self.name = name
        self.gamepath = gamepath
        self.dtdpath = dtdpath
        try:
            self.dtd = libxml2.parseDTD(None, os.path.join(self.dtdpath, 'memosono.dtd'))
        except libxml2.parserError, e:
            _logger.error('No memosono.dtd found ' +str(e))
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
                for elem in res:
                    attributes = elem.get_properties()
                    pair = []
                    idpair = 0
                    for attribute in attributes:
                        if(attribute.name == 'text'):
                            pass
                        if(attribute.name == 'id'):
                            idpair = int(attribute.content)
                        if(attribute.name == 'mother'):
                            pair.append(attribute.content)
                        if(attribute.name == 'child'):
                            pair.append(attribute.content)
                        if(attribute.name == 'color'):
                            pair.append(int(attribute.content))
                        if( elem.name == 'memosono' ):    
                            self.name = attribute.content            
                        if( elem.name != 'memosono' ):
                            self.pairs[idpair] = pair
                xpa.xpathFreeContext()
            else:
                _logger.error('Error in validation of the file')
            doc.freeDoc()
        except libxml2.parserError, e:
            _logger.error('Error parsing file ' +str(e))

            
    def save(self, filename):
        ''' saves the configuration to an xml file '''
        doc = libxml2.newDoc("1.0")
        root = doc.newChild(None, "memosono", None)
        root.setProp("name", self.name)
        for key in self.pairs:
            
            elem = root.newChild(None, "pair", None)
            elem.setProp("id", key)
            elem.setProp("mother", self.pairs[key][0])
            elem.setProp("child", self.pairs[key][1])
            elem.setProp("color", self.pairs[key][2])
        
        if doc.validateDtd(self.ctxt, self.dtd):
            doc.saveFormatFile(filename, 1)
        doc.freeDoc()    


    def def_grid(self):
        ''' create the grid for the play from the pairs information
        and shuffles the grid so they always appear in a different
        place 
        '''
        _logger.debug(' pairs: %s', self.pairs)
        for key in self.pairs.iterkeys():
            self.grid.append([key, 0, 0])
            self.grid.append([key, 1, 0])
        
        random.shuffle(self.grid)
        _logger.debug(' grid: %s', self.grid)


    def gettile(self, tilenum):
        ''' gets the information of an object associated with a tile number '''
        pairkey, moch, state = self.grid[tilenum]
        obj = os.path.join(IMAGES_PATH, self.pairs[pairkey][moch])
        color = self.pairs[pairkey][2]
        return (obj, color)


    def same(self, a, b):
        ''' checks wether two tiles are matching '''
        pairkeya, moch, state = self.grid[a]
        pairkeyb, moch, state = self.grid[b]
        return (pairkeya == pairkeyb)


    
