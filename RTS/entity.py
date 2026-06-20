import pygame
import math

class Entity():
    def __init__(self, world, type, pos, w, h):
        self.world = world
        self.type = type
        self.pos = pos
        self.w = w
        self.h = h
        self.image = pygame.Surface((self.w, self.h))
        self.killed = 0

    def update(self, events):
        pass

    def draw(self, screen):
        pos = [
            round((self.pos[0] - self.world.cam_pos[0] - self.w/2) * self.world.zoom + self.world.display_W / 2),
            round((self.pos[1] - self.world.cam_pos[1] - self.h/2) * self.world.zoom + self.world.display_H / 2)
        ]
        screen.blit(pygame.transform.scale(self.image, (self.w * self.world.zoom, self.h * self.world.zoom)), pos)

    def kill(self):
        if not self.killed:
            self.world.objects.remove(self)
        self.killed = 1

    def move(self, speed, rotate):
        if not self.collide(0, 0)[0]:
            dx = math.cos(rotate) * speed
            dy = math.sin(rotate) * speed
            self.pos[0] += dx
            collide_x = self.collide((dx < 0)*2-1, 0)
            if collide_x[0]:
                if dx > 0:
                    self.pos[0] = collide_x[1] - self.w/2
                elif dx < 0:
                    self.pos[0] = collide_x[1] + self.w/2
            self.pos[1] += dy
            collide_y = self.collide(0, (dy < 0)*2-1)
            if collide_y[0]:
                if dy > 0:
                    self.pos[1] = collide_y[2] - self.h/2
                elif dy < 0:
                    self.pos[1] = collide_y[2] + self.h/2

    def collide(self, spx, spy):#spx, spy: 1 - движется влево, 0 - не движется, -1 - движется вправо
        if self.pos[0] < self.w/2 or self.pos[1] < self.h/2:#со стенами
            return(1, 0, 0)
        if self.pos[0] > self.world.w * 16 - self.w/2 or self.pos[1] > self.world.h * 16 - self.h/2:
            return(1, self.world.w * 16, self.world.h * 16)
        #
        count = [max(math.ceil(self.w / 16), 2), max(math.ceil(self.h / 16), 2)]#с блоками
        centpos = [int(self.pos[0] // 16), int(self.pos[1] // 16)]
        for x in range(int(centpos[0] - count[0] / 2), int(centpos[0] + count[0] / 2) + 1, 1):
            for y in range(int(centpos[1] - count[1] / 2), int(centpos[1] + count[1] / 2) + 1, 1):
                if x >= 0 and x < self.world.w and y >= 0 and y < self.world.h:
                    if self.world.field[x][y].has_hitbox and self.collide_block(x * 16, y * 16):
                        return(1, x * 16 + 16 * (spx/2+0.5), y * 16 + 16 * (spy/2+0.5))
        #
        lobj = None
        lpos = 0
        if spx == 1 or spy == 1:
            lpos = -9999
        elif spx == -1 or spy == -1:
            lpos = 99999999999
        if self.type != "bullet":
            for obj in self.world.objects:#с другими юнитами
                if self.entity_collide(obj) and obj.type != "bullet":
                    if spx == 0 and spy == 0:
                        return (1, obj.pos[0] + obj.w / 2 * spx, obj.pos[1] + obj.h / 2 * spy)
                    if spx == 1:#влево
                        if obj.pos[0] > lpos:
                            lpos = obj.pos[0]
                            lobj = obj
                    elif spx == -1:#вправо
                        if obj.pos[0] < lpos:
                            lpos = obj.pos[0]
                            lobj = obj
                    #
                    if spy == 1:#вверх
                        if obj.pos[1] > lpos:
                            lpos = obj.pos[1]
                            lobj = obj
                    elif spy == -1:#вниз
                        if obj.pos[1] < lpos:
                            lpos = obj.pos[1]
                            lobj = obj
        if lobj != None:
            return (1, lobj.pos[0] + lobj.w / 2 * spx, lobj.pos[1] + lobj.h / 2 * spy)
        return(0, 0, 0)

    def collide_block(self, bl_x, bl_y):
        if self.pos[0] > bl_x - self.w/2 and self.pos[0] < bl_x + 16 + self.w/2 and self.pos[1] > bl_y - self.h/2 and self.pos[1] < bl_y + 16 + self.h/2:
            return(1)
        return(0)

    def entity_collide(self, obj):
        if obj != self:
            if self.pos[0] > obj.pos[0] - obj.w/2 - self.w/2 and self.pos[0] < obj.pos[0] + obj.w/2 + self.w/2 and \
               self.pos[1] > obj.pos[1] - obj.h/2 - self.h/2 and self.pos[1] < obj.pos[1] + obj.h/2 + self.h/2:
                return(1)
        return(0)