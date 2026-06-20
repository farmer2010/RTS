from blocks.block import *
from textures import *

class Stone(Block):
    def __init__(self, world, pos):
        Block.__init__(self, world, pos)
        self.image = pygame.Surface((16, 16))
        self.image.blit(stone_img, (0, 0))