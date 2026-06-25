from blocks.block import Block
from textures import *
from random import randint as rand

class Conveyor(Block):
    def __init__(self, world, pos, rotate=0):
        Block.__init__(self, world, "conveyor", pos)
        self.item1 = None
        self.item2 = None
        self.rotate = rotate
        self.image = conveyors[0][0]
        self.has_hitbox = False
        self.movelist = [
            [0, -1],
            [1, 0],
            [0, 1],
            [-1, 0]
        ]

    def set_item(self, item):
        if self.world.phase == 0:
            if self.item1 != None:
                return(0)
            self.item1 = item
        else:
            if self.item2 != None:
                return(0)
            self.item2 = item
        return(1)

    def take_item(self, item):#для передачи предметов конвейерами
        if self.world.phase == 0:
            if self.item2 == None:
                self.item2 = item
                return(1)
        else:
            if self.item1 == None:
                self.item1 = item
                return(1)
        return(0)

    def get_item(self):
        if self.world.phase == 0:
            return(self.item1)
        else:
            return(self.item2)

    def clear_item(self):
        if self.world.phase == 0:
            self.item1 = None
        else:
            self.item2 = None

    def move_item(self):
        pos = [self.pos[0] + self.movelist[self.rotate][0], self.pos[1] + self.movelist[self.rotate][1]]
        if self.world.test_for_block_pos(pos):
            if self.world.field[pos[0]][pos[1]].type == "conveyor" and self.world.field[pos[0]][pos[1]].rotate != (self.rotate + 2) % 4:
                item = self.get_item()
                if item != None:
                    if self.world.field[pos[0]][pos[1]].take_item(item):
                        item[0] = pos
                        item[2] = self.world.field[pos[0]][pos[1]]
                        self.clear_item()
                        return
                else:
                    pass
        if self.world.phase == 0:
            self.item2 = self.item1
            self.item1 = None
        else:
            self.item1 = self.item2
            self.item2 = None

    def get_image(self):
        c1 = 0
        c2 = 0
        c3 = 0
        pos1 = [self.pos[0] + self.movelist[(self.rotate - 1) % 4][0], self.pos[1] + self.movelist[(self.rotate - 1) % 4][1]]
        if self.world.test_for_block_pos(pos1):
            if self.world.field[pos1[0]][pos1[1]].type == "conveyor" and self.world.field[pos1[0]][pos1[1]].rotate == (self.rotate + 1) % 4:
                c1 = 1
        #
        pos2 = [self.pos[0] + self.movelist[(self.rotate - 2) % 4][0], self.pos[1] + self.movelist[(self.rotate - 2) % 4][1]]
        if self.world.test_for_block_pos(pos2):
            if self.world.field[pos2[0]][pos2[1]].type == "conveyor" and self.world.field[pos2[0]][pos2[1]].rotate == self.rotate:
                c2 = 1
        #
        pos3 = [self.pos[0] + self.movelist[(self.rotate + 1) % 4][0], self.pos[1] + self.movelist[(self.rotate + 1) % 4][1]]
        if self.world.test_for_block_pos(pos3):
            if self.world.field[pos3[0]][pos3[1]].type == "conveyor" and self.world.field[pos3[0]][pos3[1]].rotate == (self.rotate - 1) % 4:
                c3 = 1
        #
        return(conveyors[self.rotate][c1 * 4 + c2 * 2 + c3])

    def remove_block(self):
        Block.remove_block(self)
        if self.item1 != None:
            self.world.items.remove(self.item1)
        if self.item2 != None:
            self.world.items.remove(self.item2)