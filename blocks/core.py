from blocks.block import *

class Core(Block):
    def __init__(self, world, pos, player):
        Block.__init__(self, world, pos, "core", player, health=2000)
        self.index = (0, 0)
        self.is_conveyor = 1
        self.is_construction = 1

    def set_item(self, item):
        self.player.resources[item[0]] += 1
        if item in self.world.items:
            self.world.items.remove(item)
        return(1)

    def can_take_item(self, rotate):
        return(True)