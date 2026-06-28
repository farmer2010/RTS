from units.unit import *
import blocks


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
        if self.timer >= 30:
            self.timer = 0
            if not dig and self.command == None:
                if self.task != None:
                    self.player.task_units[self.task[0]][self.task[1]] = None
                    self.task = None
                self.update_task()

    def dig(self):
        pos = [int(self.pos[0] / 16), int(self.pos[1] / 16)]
        for i in range(8):
            x, y = pos[0] + self.movelist8[i][0], pos[1] + self.movelist8[i][1]
            if self.world.test_for_block_pos((x, y)):
                if self.player.task_field[x][y] == 1:
                    self.world.field[x][y].progress -= self.world.field[x][y].mining_speed
                    if self.world.field[x][y].progress <= 0:
                        self.player.task_field[x][y] = 0
                        for c in blocks.cost[self.world.field[x][y].type]:
                            if self.world.field[x][y].is_construction:
                                self.player.resources[c[0]] += math.ceil(c[1] / 2)
                            else:
                                self.player.resources[c[0]] += c[1]
                        self.world.field[x][y].remove_block()
                    self.world.chunks[int(x // 16)][int(y // 16)].image_changes = 1
                    return(1)
                elif self.player.task_field[x][y] != 0:
                    enough = 1
                    for c in blocks.cost[self.player.task_field[x][y][0]]:
                        if self.player.resources[c[0]] < c[1]:
                            enough = 0
                    if enough:
                        if self.world.field[x][y].type == "air":
                            self.world.field[x][y] = blocks.WorkInProgress(self.world, (x, y))
                        elif self.world.field[x][y].type == "work in progress" and len(self.world.unit_field[x][y]) == 0:
                            self.world.field[x][y].progress += 1
                            if self.world.field[x][y].progress >= blocks.build_time[self.player.task_field[x][y][0]]:
                                blocks.set_block(self.world, (x, y), self.player, self.player.task_field[x][y][0], self.player.task_field[x][y][1])
                                for c in blocks.cost[self.player.task_field[x][y][0]]:
                                    self.player.resources[c[0]] -= c[1]
                                self.player.task_field[x][y] = 0
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
        #
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
                        enough = 1
                        if self.player.task_field[x][y] != 1:
                            for c in blocks.cost[self.player.task_field[x][y][0]]:
                                if self.player.resources[c[0]] < c[1]:
                                    enough = 0
                        if enough and len(self.world.unit_field[x][y]) == 0:
                            f1 = self.world.test_for_block_pos((x, y - 1)) and not self.world.field[x][y - 1].has_hitbox
                            f2 = self.world.test_for_block_pos((x, y + 1)) and not self.world.field[x][y + 1].has_hitbox
                            f3 = self.world.test_for_block_pos((x - 1, y)) and not self.world.field[x - 1][y].has_hitbox
                            f4 = self.world.test_for_block_pos((x + 1, y)) and not self.world.field[x + 1][y].has_hitbox
                            if f1 or f2 or f3 or f4:
                                self.move_command((x, y), move_to_close=1)
                                if self.command != None:
                                    self.world.player.task_units[x][y] = self
                                    self.task = (x, y)
                                    return
                #
            if i % 2 == 1:
                length += 1
            rotate = (rotate + 1) % 4