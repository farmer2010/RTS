from blocks.block import *
from textures import *

class Sand(Block):
    def __init__(self, world, pos):
        Block.__init__(self, world, "sand", pos)
        self.image = pygame.Surface((16, 16))
        self.image.blit(sand_img, (0, 0))
        self.has_hitbox = False
        self.speed = 0.7