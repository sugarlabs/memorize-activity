import libxml2
import os
import logging
import random
import gobject

IMAGES_PATH = 'games/drumgit/images'
GAME_PATH = 'games/drumgit'

_logger = logging.getLogger('model')


class Pair(gobject.GObject):    
    __gproperties__ = {
        'aimg'    : (str, None, None, None, gobject.PARAM_READWRITE),
        'asnd'    : (str, None, None, None, gobject.PARAM_READWRITE),
        'bimg'    : (str, None, None, None, gobject.PARAM_READWRITE),        
        'bsnd'    : (str, None, None, None, gobject.PARAM_READWRITE),
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
        elif pspec.name == "bimg":
            return self._properties["bimg"]
        elif pspec.name == "bsnd":
            return self._properties["bsnd"]
        elif pspec.name == "color":
            return self._properties["color"]

    def set_property(self, name, value):
        if name == 'aimg':
            self._properties['aimg'] = value
        elif name == "asnd":
            self._properties["asnd"] = value
        elif name == "bimg":
            self._properties["bimg"] = value
        elif name == "bsnd":
            self._properties["bsnd"] = value
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
                self.idpair = 0
                for elem in res:
                    attributes = elem.get_properties()
                    pair = Pair()
                    for attribute in attributes:
                        if(attribute.name == 'text'):
                            pass
                        else:
                            pass
                            pair.set_property(attribute.name, attribute.content)
                    if( elem.name == 'pair' ):
                        self.pairs[self.idpair] = pair
                        self.idpair+=1
                    elif( elem.name == 'memosono' ):    
                        self.name = attribute.content            
                    
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
            if self.pairs[key].props.aimg != None:
                elem.setProp("aimg", self.pairs[key].props.aimg)
            if self.pairs[key].props.asnd != None:
                elem.setProp("asnd", self.pairs[key].props.asnd)
            if self.pairs[key].props.bimg != None:
                elem.setProp("bimg", self.pairs[key].props.bimg)
            if self.pairs[key].props.bsnd != None:
                elem.setProp("bsnd", self.pairs[key].props.bsnd)
            elem.setProp("color", str(self.pairs[key].props.color))
        
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


    

if __name__ == '__main__':
    model = Model(GAME_PATH, os.path.dirname(__file__))
    model.read('drumgit.mson')
    print '%s' %model.pairs[0].props.color
    print '%s' %model.pairs[1]._properties
    print '%s' %model.pairs[2]._properties

    model.def_grid()
    print model.grid
    #model.save('/tmp/mod.txt')
