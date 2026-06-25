from blocks.block import Block
from textures import *
from random import randint as rand

class Router(Block):
    def __init__(self, world, pos):
        Block.__init__(self, world, "router", pos)
        self.item = None
        self.image = router_img
        self.has_hitbox = False
        self.movelist = [
            [0, -1],
            [1, 0],
            [0, 1],
            [-1, 0]
        ]
        self.is_conveyor = 1
        self.index = 0

    def set_item(self, item):
        if self.item == None:
            self.item = item
            return(1)
        return(0)

    def clear_item(self):
        if self.item != None:
            self.world.items.remove(self.item)
        self.item = None

    def move_item(self):
        for i in range(4):
            pos = [self.pos[0] + self.movelist[self.index][0], self.pos[1] + self.movelist[self.index][1]]
            if self.world.test_for_block_pos(pos):
                if self.world.field[pos[0]][pos[1]].is_conveyor and self.world.field[pos[0]][pos[1]].is_take_item(self.index):
                    item = self.item
                    if item != None:
                        if self.world.field[pos[0]][pos[1]].set_item(item):
                            item[1] = self.world.field[pos[0]][pos[1]]
                            self.item = None
                            self.index = ((self.index + 1) % 4)
                            return
            self.index  = ((self.index + 1) % 4)

    def remove_block(self):
        Block.remove_block(self)
        if self.item != None:
            self.world.items.remove(self.item)

    def is_connect_conveyor(self, rotate):
        return(True)

    def is_take_item(self, rotate):
        return(True)