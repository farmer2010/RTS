from blocks.block import Block
from textures import *

class Conveyor(Block):
    def __init__(self, world, pos):
        Block.__init__(self, world, "conveyor", pos)
        self.item1 = None
        self.item2 = None
        self.rotate = 0
        self.image = pygame.Surface((16, 16))
        self.image = grass_img
        self.has_hitbox = False