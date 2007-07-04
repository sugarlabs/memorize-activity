

class GameState(object):
    ''' Used by the leader of the game to keep track of the game state 
    '''

    def __init__(self):
        self.player_active = 0
        self.points = {}
        self.turn = 0
        self.selected = 0
        
        
