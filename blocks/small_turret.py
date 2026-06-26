from blocks.block import Block
from textures import *
from units import *

class SmallTurret(Block):#турель 1*1
    def __init__(self, world, pos, player, type="stone turret"):
        if type == "stone turret":
            h = 80
        Block.__init__(self, world, type, pos, player=player, health=h)
        self.is_construction = 1
        self.image = small_turret_img
        self.unit = TurretUnit(self.world, self.player, [self.pos[0] * 16 + 8, self.pos[1] * 16 + 8], self.type)
        self.world.objects.append(self.unit)

    def remove_block(self):
        Block.remove_block(self)
        self.world.objects.remove(self.unit)