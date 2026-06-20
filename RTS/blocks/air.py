from blocks.block import *
from textures import *

class Air(Block):
    def __init__(self, world, pos):
        Block.__init__(self, world, pos)
        self.image = pygame.Surface((16, 16))
        self.image.blit(air_img, (0, 0))
        self.has_hitbox = 0