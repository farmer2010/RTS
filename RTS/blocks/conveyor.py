from blocks.block import Block
from textures import *
from random import randint as rand

class Conveyor(Block):
    def __init__(self, world, pos, rotate=0):
        Block.__init__(self, world, "conveyor", pos)
        self.item = None
        self.rotate = rotate
        self.image = conveyors[0][0]
        self.has_hitbox = False
        self.movelist = [
            [0, -1],
            [1, 0],
            [0, 1],
            [-1, 0]
        ]
        self.is_conveyor = 1

    def set_item(self, item, rotate):
        if self.item == None:
            self.item = item
            return(1)
        return(0)

    def clear_item(self):
        if self.item != None:
            self.world.items.remove(self.item)
        self.item = None

    def move_item(self, item):
        pos = [self.pos[0] + self.movelist[self.rotate][0], self.pos[1] + self.movelist[self.rotate][1]]
        if self.world.test_for_block_pos(pos):
            if self.world.field[pos[0]][pos[1]].is_conveyor and self.world.field[pos[0]][pos[1]].can_take_item(self.rotate):
                if item != None and item is self.item:
                    if self.world.field[pos[0]][pos[1]].set_item(item, self.rotate):
                        item[1] = self.world.field[pos[0]][pos[1]]
                        self.item = None

    def get_image(self):
        c1 = 0
        c2 = 0
        c3 = 0
        pos1 = [self.pos[0] + self.movelist[(self.rotate - 1) % 4][0], self.pos[1] + self.movelist[(self.rotate - 1) % 4][1]]
        if self.world.test_for_block_pos(pos1):
            if self.world.field[pos1[0]][pos1[1]].is_connect_conveyor((self.rotate - 1) % 4):
                c1 = 1
        #
        pos2 = [self.pos[0] + self.movelist[(self.rotate - 2) % 4][0], self.pos[1] + self.movelist[(self.rotate - 2) % 4][1]]
        if self.world.test_for_block_pos(pos2):
            if self.world.field[pos2[0]][pos2[1]].is_connect_conveyor((self.rotate - 2) % 4):
                c2 = 1
        #
        pos3 = [self.pos[0] + self.movelist[(self.rotate + 1) % 4][0], self.pos[1] + self.movelist[(self.rotate + 1) % 4][1]]
        if self.world.test_for_block_pos(pos3):
            if self.world.field[pos3[0]][pos3[1]].is_connect_conveyor((self.rotate + 1) % 4):
                c3 = 1
        #
        return(conveyors[self.rotate][c1 * 4 + c2 * 2 + c3])

    def remove_block(self):
        Block.remove_block(self)
        if self.item != None:
            self.world.items.remove(self.item)

    def is_connect_conveyor(self, rotate):
        return(self.rotate == (rotate + 2) % 4)

    def can_take_item(self, rotate):
        return(self.rotate == rotate or self.rotate == (rotate + 1) % 4 or self.rotate == (rotate - 1) % 4)