from blocks.block import Block
from textures import *
from random import randint as rand


class Wall(Block):
    def __init__(self, world, pos, player, type="stone wall"):
        Block.__init__(self, world, type, pos, player=player)
        self.is_construction = 1

    def get_image(self):
        if self.type == "stone wall":
            return(stone_wall_img)
        elif self.type == "iron wall":
            return(iron_wall_img)
