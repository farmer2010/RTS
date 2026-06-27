from blocks.block import Block
from textures import *

class StoneFloor(Block):
    def __init__(self, world, pos):
        Block.__init__(self, world, "stone floor", pos)
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.image.blit(stone_img, (0, 0))
        f = pygame.Surface((16, 16), pygame.SRCALPHA)
        f.fill((0, 0, 0, 85))
        self.image.blit(f, (0, 0))
        self.has_hitbox = False
        self.speed = 1