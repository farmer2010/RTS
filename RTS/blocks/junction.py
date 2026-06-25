from blocks.block import Block
from textures import *
from random import randint as rand

class Junction(Block):
    def __init__(self, world, pos):
        Block.__init__(self, world, "junction", pos)
        self.items = [None, None, None, None]
        self.image = junction_img
        self.has_hitbox = False
        self.movelist = [
            [0, -1],
            [1, 0],
            [0, 1],
            [-1, 0]
        ]
        self.is_conveyor = 1

    def set_item(self, item, rotate):
        if self.items[rotate] == None:
            self.items[rotate] = item
            return(1)
        return(0)

    def clear_item(self):
        for i in range(4):
            if self.items[i] != None:
                self.world.items.remove(self.items[i])
                self.items[i] = None

    def move_item(self, item):
        for i in range(4):
            if item != None and item == self.items[i]:
                pos = [self.pos[0] + self.movelist[i][0], self.pos[1] + self.movelist[i][1]]
                if self.world.test_for_block_pos(pos):
                    if self.world.field[pos[0]][pos[1]].is_conveyor and self.world.field[pos[0]][pos[1]].is_take_item(i):
                        if self.world.field[pos[0]][pos[1]].set_item(item, i):
                            item[1] = self.world.field[pos[0]][pos[1]]
                            self.items[i] = None
                return

    def remove_block(self):
        Block.remove_block(self)
        for i in range(4):
            if self.items[i] != None:
                self.world.items.remove(self.items[i])
                self.items[i] = None

    def is_connect_conveyor(self, rotate):
        return(True)

    def is_take_item(self, rotate):
        return(True)