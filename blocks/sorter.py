from blocks.block import Block
from textures import *
from random import randint as rand

class Sorter(Block):
    def __init__(self, world, pos, player, type="sorter"):
        Block.__init__(self, world, type, pos, player=player)
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
        self.rotate = 0
        self.config = "stone"
        self.is_construction = 1

    def set_item(self, item, rotate):
        if self.item == None:
            self.item = item
            self.rotate = rotate
            return(1)
        return(0)

    def clear_item(self):
        if self.item != None:
            self.world.items.remove(self.item)
        self.item = None

    def move_item(self, item):
        if item != None and item is self.item:
            if (item[0] == self.config and self.type == "sorter") or (item[0] != self.config and self.type == "inverted sorter"):#передаем вперед
                pos = [self.pos[0] + self.movelist[self.rotate][0], self.pos[1] + self.movelist[self.rotate][1]]  # вперед
                if self.world.test_for_block_pos(pos):
                    if self.world.field[pos[0]][pos[1]].is_conveyor and self.world.field[pos[0]][pos[1]].can_take_item(self.rotate):
                        if self.world.field[pos[0]][pos[1]].set_item(item, self.rotate):
                            item[1] = self.world.field[pos[0]][pos[1]]
                            self.item = None
            else:#передаем по бокам
                for i in range(2):
                    pos = [self.pos[0] + self.movelist[(self.rotate + self.index * 2 - 1) % 4][0], self.pos[1] + self.movelist[(self.rotate + self.index * 2 - 1) % 4][1]]  # по бокам
                    if self.world.test_for_block_pos(pos):
                        if self.world.field[pos[0]][pos[1]].is_conveyor and self.world.field[pos[0]][pos[1]].can_take_item((self.rotate + self.index * 2 - 1) % 4):
                            if self.world.field[pos[0]][pos[1]].set_item(item, (self.rotate + self.index * 2 - 1) % 4):
                                item[1] = self.world.field[pos[0]][pos[1]]
                                self.item = None
                                self.index = (self.index + 1) % 2
                                return
                    self.index = (self.index + 1) % 2

    def remove_block(self):
        Block.remove_block(self)
        if self.item != None:
            self.world.items.remove(self.item)

    def is_connect_conveyor(self, rotate):
        return(True)

    def can_take_item(self, rotate):
        return(True)

    def get_image(self):
        if self.type == "sorter":
            return(sorter_images[self.config])
        elif self.type == "inverted sorter":
            return (inverted_sorter_images[self.config])

    def action(self):
        if self.player == self.world.player:
            if self.config == "stone":
                self.config = "coal"
            elif self.config == "coal":
                self.config = "iron"
            elif self.config == "iron":
                self.config = "copper"
            elif self.config == "copper":
                self.config = ""
            elif self.config == "":
                self.config = "stone"