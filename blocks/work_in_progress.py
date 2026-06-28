from blocks.block import *
from textures import *

class WorkInProgress(Block):#технический блок, отвечающий за строительство блоков юнитами
    def __init__(self, world, pos):
        Block.__init__(self, world, "work in progress", pos)
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.has_hitbox = 0
        self.progress = 0