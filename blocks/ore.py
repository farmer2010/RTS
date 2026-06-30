from blocks import *
from textures import *

class Ore(Block):
    def __init__(self, world, pos, type):
        Block.__init__(self, world, type, pos)
        if type == "coal ore":
            self.image = block_coal_ore_img
        elif type == "iron ore":
            self.image = block_iron_ore_img
        elif type == "copper ore":
            self.image = block_copper_ore_img
        self.can_mined = 1