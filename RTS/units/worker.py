from units.unit import *
from blocks import *


class Worker(Unit):
    def __init__(self, world, player, pos):
        Unit.__init__(self, world, player, "worker", pos, 10, 10)
        self.image.fill((30, 100, 255))

    def update(self, events):
        Unit.update(self, events)
        self.dig()

    def dig(self):
        pos = [int(self.pos[0] / 16), int(self.pos[1] / 16)]
        for x in range(pos[0] - 1, pos[0] + 2):
            for y in range(pos[1] - 1, pos[1] + 2):
                if self.world.test_for_block_pos((x, y)):
                    if self.world.field[x][y].can_mined and self.player.task_field[x][y] == 1:
                        self.world.field[x][y].progress -= 5
                        if self.world.field[x][y].progress <= 0:
                            self.player.task_field[x][y] = 0
                            self.world.field[x][y] = Air(self.world, pos)
                            self.world.chunks[int(x // 16)][int(y // 16)].update_image()