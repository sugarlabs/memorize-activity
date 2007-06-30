import gtk
import os

from playview import PlayView
from model import Game

        
class Test(object):
    def __init__(self):

        self.games = {}
        os.path.walk(os.path.join(os.path.dirname(__file__), 'games'), self._find_games, None)

        gamelist = self.games.keys()
        gamelist.sort()

        print 'gamelist: %s' %gamelist
        print 'pairs: %s' %self.games[gamelist[0]].pairs
        
        self.pv = PlayView(self.games[gamelist[0]].pairs)

        window = gtk.Window()
        window.connect('destroy', gtk.main_quit)
        window.connect('key-press-event', self.key_press_cb)
        window.add(self.pv)
        window.show_all()
        try:
            gtk.main()
        except KeyboardInterupt:
            pass
        
    def key_press_cb(self, window, event):
        if gtk.gdk.keyval_name(event.keyval) in ('Escape', 'q'):
            gtk.main_quit()

    def _find_games(self, arg, dirname, names):
        for name in names:
            if name.endswith('.mson'): 
                game = Game(dirname, os.path.dirname(__file__))
                game.read(name)
                self.games[name.split('.mson')[0]] = game


if __name__ == '__main__':
    Test()

