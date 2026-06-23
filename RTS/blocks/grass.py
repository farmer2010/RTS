from blocks.block import *
from textures import *

class Grass(Block):
    def __init__(self, world, pos):
        Block.__init__(self, world, "grass", pos)
        self.image = pygame.Surface((16, 16))
        self.image.blit(grass_img, (0, 0))
        self.has_hitbox = False
        self.speed = 0.9