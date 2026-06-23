from blocks.block import *
from textures import *

class Stone(Block):
    def __init__(self, world, pos):
        Block.__init__(self, world, "stone", pos)
        self.image = pygame.Surface((16, 16))
        self.image = stone_img
        self.can_mined = 1