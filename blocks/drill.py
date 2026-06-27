from blocks.block import Block
from textures import *
from random import randint as rand
from units import *

class Drill(Block):
    def __init__(self, world, pos, player, type="drill"):
        Block.__init__(self, world, type, pos, player=player)
        self.item = None
        self.config = ""
        self.timer = 0
        self.items = 0
        ore = self.world.ore_field[self.pos[0]][self.pos[1]]
        if ore != None:
            self.config = ore[0]
        if self.type == "drill":
            self.mine_speed = {
                "stone" : 120,
                "coal" : 180,
            }
        self.image = router_img
        self.has_hitbox = True
        self.movelist = [
            [0, -1],
            [1, 0],
            [0, 1],
            [-1, 0]
        ]
        self.is_conveyor = 1
        self.index = 0
        self.is_construction = 1
        self.unit = DrillUnit(self.world, self.player, self)
        self.world.objects.append(self.unit)

    def set_item(self, item, rotate=0):
        if self.item == None:
            self.item = item
            return(1)
        return(0)

    def clear_item(self):
        if self.item != None:
            self.world.items.remove(self.item)
        self.item = None

    def move_item(self, item):
        for i in range(4):
            pos = [self.pos[0] + self.movelist[self.index][0], self.pos[1] + self.movelist[self.index][1]]
            if self.world.test_for_block_pos(pos):
                if self.world.field[pos[0]][pos[1]].is_conveyor and self.world.field[pos[0]][pos[1]].can_take_item(self.index):
                    if item != None and item is self.item:
                        if self.world.field[pos[0]][pos[1]].set_item(item, i):
                            item[1] = self.world.field[pos[0]][pos[1]]
                            self.item = None
                            self.index = ((self.index + 1) % 4)
                            return
            self.index  = ((self.index + 1) % 4)

    def remove_block(self):
        Block.remove_block(self)
        self.world.objects.remove(self.unit)
        if self.item != None:
            self.world.items.remove(self.item)

    def is_connect_conveyor(self, rotate):
        return(True)

    def get_image(self):
        ore = self.world.ore_field[self.pos[0]][self.pos[1]]
        if ore != None:
            return (drill_images[ore[0]])
        else:
            return(drill_images[""])