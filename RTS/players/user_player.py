from players.player import *

class UserPlayer(Player):#игрок, контролируемый пользователем
    def __init__(self, world):
        Player.__init__(self, world)