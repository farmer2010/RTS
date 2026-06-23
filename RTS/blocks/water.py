from blocks.block import *
from textures import *


class Water(Block):
    def __init__(self, world, pos):
        Block.__init__(self, world, "water", pos)
        self.image = pygame.Surface((16, 16))
        self.image = water_img