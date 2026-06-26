from units.unit import *

class TurretUnit(Unit):#пушка турели
    def __init__(self, world, player, pos, type, scale=16, radius=15):
        Unit.__init__(self, world, player, "turret unit", pos, scale, scale, fog_radius=radius, speed=0, health=400)
        self._class = "turret unit"
        self.can_shoot = 1
        self.type = type
        if type == "stone turret":
            self.image = stone_turret_img
        self.rotate = 0

    def update(self, events):
        if self.can_shoot and self.reload_timer == 0 and self.target == None:
            min_dist = 99999999
            for obj in self.world.objects:
                if obj._class == "unit" and obj.player != self.player:
                    dist = (obj.pos[0] - self.pos[0]) ** 2 + (obj.pos[1] - self.pos[1]) ** 2
                    if dist <= (self.fog_radius * 16) ** 2 and dist < min_dist:
                        self.target = obj
                        min_dist = dist
            #
            if self.target == None:
                x, y = int(self.pos[0] // 16), int(self.pos[1] // 16)
                rot = 0
                length = 1
                stop = 0
                for i in range(self.fog_radius * 4 + 1):
                    if i == self.fog_radius * 4:
                        length -= 1
                    for j in range(length):
                        x += self.movelist4[rot][0]
                        y += self.movelist4[rot][1]
                        #
                        if self.world.test_for_block_pos((x, y)):
                            bl = self.world.field[x][y]
                            if bl.is_construction and bl.player != self.player:
                                if (bl.pos[0] * 16 - self.pos[0]) ** 2 + (bl.pos[1] * 16 - self.pos[1]) ** 2 <= (self.fog_radius * 16) ** 2:
                                    self.target = bl
                                    stop = 1
                                    break
                        #
                    if stop:
                        break
                    if i % 2 == 1:
                        length += 1
                    rot = (rot + 1) % 4
        #
        #
        if self.target != None and self.target._class == "unit" and ((self.target.pos[0] - self.pos[0]) ** 2 + (self.target.pos[1] - self.pos[1]) ** 2 > (self.fog_radius * 16) ** 2 or self.target.killed):
            self.target = None
        if self.target != None and self.target._class == "block" and ((self.target.pos[0] * 16 - self.pos[0]) ** 2 + (self.target.pos[1] * 16 - self.pos[1]) ** 2 > (self.fog_radius * 16) ** 2 or self.target.killed):
            self.target = None
        if self.target != None and self.reload_timer == 0:
            if self.target._class == "unit":
                rotate = math.atan2(self.target.pos[1] - self.pos[1], self.target.pos[0] - self.pos[0])
            elif self.target._class == "block":
                rotate = math.atan2(self.target.pos[1] * 16 + 8 - self.pos[1], self.target.pos[0] * 16 + 8 - self.pos[0])
            self.rotate = rotate
            self.world.objects.append(Projectile(self.world, self.player, self.pos.copy(), 5, 5, rotate, 5, self.fog_radius*16, 10))
            self.reload_timer = self.reload
        if self.reload_timer > 0:
            self.reload_timer -= 1

    def draw(self, screen):
        if self.target != None:
            if self.target._class == "unit":
                self.rotate = math.atan2(self.target.pos[1] - self.pos[1], self.target.pos[0] - self.pos[0])
            elif self.target._class == "block":
                self.rotate = math.atan2(self.target.pos[1] * 16 + 8 - self.pos[1], self.target.pos[0] * 16 + 8 - self.pos[0])
        img = pygame.transform.scale(self.image, (self.w * self.world.zoom, self.h * self.world.zoom))
        img = pygame.transform.rotate(img, 270 - self.rotate * 57.296)
        pos = self.world.game_to_display(self.pos)
        screen.blit(img, [pos[0] - img.get_width() / 2, pos[1] - img.get_height() / 2])