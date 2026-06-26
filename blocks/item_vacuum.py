from blocks.block import Block
from textures import *
from random import randint as rand

class ItemVacuum(Block):
    def __init__(self, world, pos, rotate=0):
        Block.__init__(self, world, "item vacuum", pos)
        self.rotate = rotate
        self.image.fill((255, 128, 0))
        self.has_hitbox = False
        self.is_conveyor = 1

    def set_item(self, item, rotate):
        self.world.items.remove(item)
        return(1)

    def clear_item(self):
        if self.item != None:
            self.world.items.remove(self.item)
        self.item = None

    def move_item(self, item):
        pass

    def is_connect_conveyor(self, rotate):
        return(1)

    def can_take_item(self, rotate):
        return(1)