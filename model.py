import libxml2
import os
import logging
import random

IMAGES_PATH = os.path.join(os.path.dirname(__file__),'games/drumgit/images')

class Model(object):
    def __init__(self, gamepath, dtdpath, name='noname'):
        self.name = name
        self.pairs = {}
        self.grid = []
        self.gamepath = gamepath
        self.dtdpath = dtdpath

        try:
            self.dtd = libxml2.parseDTD(None, os.path.join(self.dtdpath, 'memosono.dtd'))
        except libxml2.parserError, e:
            logging.error('No memosono.dtd found ' +str(e))
            self.dtd = None
        self.ctxt = libxml2.newValidCtxt()               
        
    def read(self, filename):
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
                logging.error('Error in validation of the file')
            doc.freeDoc()
        except libxml2.parserError, e:
            logging.error('Error parsing file ' +str(e))
            
    def save(self, filename):
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
        print 'pairs: %s' %self.pairs
        ### create grid from pairs information
        for key in self.pairs.iterkeys():
            self.grid.append((key, 0))
            self.grid.append((key, 1))
        print 'self.grid: %s'%self.grid

        ### shuffle the grid tiles
        random.shuffle(self.grid)
        print 'self.grid after shufle: %s'%self.grid

    def gettile(self, tilenum):
        pairkey, moch = self.grid[tilenum]
        obj = os.path.join(IMAGES_PATH, self.pairs[pairkey][moch])
        color = self.pairs[pairkey][2]
        # logger.debug('obj=%s color=%s'%(obj, color))
        return (obj, color)

    def same(self, a, b):
        pairkeya, moch = self.grid[a]
        pairkeyb, moch = self.grid[b]
        return (pairkeya == pairkeyb)
        
if __name__ == '__main__':
    
    print "[Read game from file] "        
    model = Model()
    model.read('memosono.xml')
    print "   name=" + model.name
    print "   pairs=%s" %model.pairs

    elemkey = '0'
    if model.pairs.has_key(elemkey):
        del model.pairs[elemkey]
        
    model.pairs['2'] = ['frettchen.jpg', 'frettchen.wav']

    print "[Write game to file] "        
    model.save('memosono.xml')
        

    
