class DrillUnit():
    def __init__(self, world, player, drill):
        self._class = "drill unit"
        self.world = world
        self.player = player
        self.drill = drill
        self.w, self.h = 12, 12
        self.pos = [self.drill.pos[0] * 16 + 8, self.drill.pos[1] * 16 + 8]

    def update(self, events):
        if self.drill.items > 0:
            itm = [self.drill.config, self.drill]
            if self.drill.set_item(itm):
                self.world.items.append(itm)
                self.drill.items -= 1
        if self.drill.has_ore:
            self.drill.timer += 1
            if self.drill.timer >= self.drill.mine_speed[self.drill.config]:
                self.drill.timer = 0
                bl = self.world.ore_field[self.drill.pos[0]][self.drill.pos[1]]
                if bl != None:
                    if bl[1] > 0:
                        itm = [self.drill.config, self.drill]
                        if self.drill.set_item(itm):
                            self.world.items.append(itm)
                            bl[1] -= 1
                        elif self.drill.items < 20:
                            self.drill.items += 1
                            bl[1] -= 1
                    else:
                        self.drill.has_ore = 0
                        self.world.ore_field[self.drill.pos[0]][self.drill.pos[1]] = None
                        self.world.chunks[int(self.drill.pos[0] / 16)][int(self.drill.pos[1] / 16)].image_changes = 1
                else:
                    self.drill.has_ore = 0

    def draw(self, screen):
        pass