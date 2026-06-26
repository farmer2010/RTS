from units.unit import *
from blocks import *


class Worker(Unit):
    def __init__(self, world, player, pos):
        Unit.__init__(self, world, player, "worker", pos, 10, 10, fog_radius=10, speed=4, health=60)
        self.image.fill((30, 100, 255))
        self.timer = 0
        self.task = None

    def update(self, events):
        Unit.update(self, events)
        dig = self.dig()
        self.timer += 1
        if self.timer >= 60:
            self.timer = 0
            if not dig and self.command == None:
                if self.task != None:
                    self.player.task_units[self.task[0]][self.task[1]] = None
                self.update_task()

    def dig(self):
        pos = [int(self.pos[0] / 16), int(self.pos[1] / 16)]
        for x in range(pos[0] - 1, pos[0] + 2):
            for y in range(pos[1] - 1, pos[1] + 2):
                if self.world.test_for_block_pos((x, y)):
                    if self.world.field[x][y].can_mined and self.player.task_field[x][y] == 1:
                        self.world.field[x][y].progress -= self.world.field[x][y].mining_speed
                        if self.world.field[x][y].progress <= 0:
                            self.player.task_field[x][y] = 0
                            self.world.field[x][y].remove_block()
                        self.world.chunks[int(x // 16)][int(y // 16)].image_changes = 1
                        return(1)
        return(0)

    def update_task(self):
        radius = 30
        cent_pos = [int(self.pos[0] // 16), int(self.pos[1] // 16)]
        moves = [
            [0, -1],
            [1, 0],
            [0, 1],
            [-1, 0]
        ]

        x, y = int(self.pos[0] // 16), int(self.pos[1] // 16)
        rotate = 0
        length = 1
        for i in range(radius * 4 + 1):
            if i == radius * 4:
                length -= 1
            for j in range(length):
                x += moves[rotate][0]
                y += moves[rotate][1]
                #
                if self.world.test_for_block_pos((x, y)):
                    if self.player.task_field[x][y] != 0 and self.player.task_units[x][y] == None:
                        f1 = self.world.test_for_block_pos((x, y - 1)) and not self.world.field[x][y - 1].has_hitbox
                        f2 = self.world.test_for_block_pos((x, y + 1)) and not self.world.field[x][y + 1].has_hitbox
                        f3 = self.world.test_for_block_pos((x - 1, y)) and not self.world.field[x - 1][y].has_hitbox
                        f4 = self.world.test_for_block_pos((x + 1, y)) and not self.world.field[x + 1][y].has_hitbox
                        if f1 or f2 or f3 or f4:
                            self.world.player.task_units[x][y] = self
                            self.move_command((x, y), move_to_close=1)
                            if self.command != None:
                                return
                #
            if i % 2 == 1:
                length += 1
            rotate = (rotate + 1) % 4