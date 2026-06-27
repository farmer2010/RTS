from blocks.block import Block
from textures import *
from units import *

class Turret(Block):#турель 1*1
    def __init__(self, world, pos, player, type="stone turret"):
        if type == "stone turret":
            h = 80
            self.ammo_type = "stone"
            self.max_items = 20
        Block.__init__(self, world, type, pos, player=player, health=h)
        self.is_construction = 1
        self.image = small_turret_img
        self.items = 0
        self.unit = TurretUnit(self.world, self.player, [self.pos[0] * 16 + 8, self.pos[1] * 16 + 8], self.type)
        self.world.objects.append(self.unit)
        self.is_conveyor = 1

    def set_item(self, item, rotate=0):
        if self.items < self.max_items and item[0] == self.ammo_type:
            self.items += 1
            self.world.items.remove(item)
            return(1)
        return(0)

    def remove_block(self):
        Block.remove_block(self)
        self.unit.kill()

    def can_take_item(self, rotate):
        return(True)