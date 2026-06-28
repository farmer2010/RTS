from blocks.block import Block
from textures import *
from random import randint as rand
from units.factory_unit import *

class Factory(Block):
    def __init__(self, world, pos, player, type="iron furnace"):
        Block.__init__(self, world, type, pos, player=player)
        self.item = None
        self.timer = 0
        self.items = {}
        if self.type == "iron furnace":
            self.image = iron_furnace_img
            self.recipe = {
                "cost": [
                    ["iron", 1],
                    ["coal", 1]
                ],
                "result": ["iron bar", 1]
            }
            self.items = {
                "iron" : 0,
                "coal" : 0,
                "iron bar" : 0
            }
            self.production_time = 90
        elif self.type == "copper furnace":
            self.image = copper_furnace_img
            self.recipe = {
                "cost": [
                    ["copper", 1],
                    ["coal", 1]
                ],
                "result": ["copper bar", 1]
            }
            self.items = {
                "copper": 0,
                "coal": 0,
                "copper bar": 0
            }
            self.production_time = 90
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
        self.unit = FactoryUnit(self.world, self.player, self)
        self.world.objects.append(self.unit)

    def set_item(self, item, rotate=0):
        if item[0] in self.items and self.items[item[0]] < 20:
            self.items[item[0]] += 1
            self.world.items.remove(item)
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

    def can_take_item(self, rotate):
        return(True)