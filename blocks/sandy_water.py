from blocks.block import *
from textures import *

class SandyWater(Block):
    def __init__(self, world, pos):
        Block.__init__(self, world, "sandy water", pos)
        self.image = pygame.Surface((16, 16))
        self.image = sandy_water_img
        self.has_hitbox = False
        self.speed = 0.25