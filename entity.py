import pygame
import math
from random import randint as rand

class Entity():
    def __init__(self, world, player, _class, pos, w, h):
        self.world = world
        self._class = _class
        self.pos = pos
        self.w = w
        self.h = h
        self.image = pygame.Surface((self.w, self.h))
        self.killed = 0
        self.player = player
        self.moved = 0#двигался ли объект на текущем шаге

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
        coll = 0
        coll_obj_s = None
        coll_obj_x = None
        coll_obj_y = None
        #
        collide_s = self.collide(0, 0)
        coll_obj_s = collide_s[3]
        if not collide_s[0]:
            dx = math.cos(rotate) * speed
            dy = math.sin(rotate) * speed
            self.pos[0] += dx
            collide_x = self.collide((dx < 0)*2-1, 0)
            if collide_x[0]:
                coll = 1
                if dx > 0.01:
                    self.pos[0] = collide_x[1] - self.w/2
                elif dx < 0.01:
                    self.pos[0] = collide_x[1] + self.w/2
                #
                if collide_x[3] != None and collide_x[3]._class == "unit" and self._class == "unit":
                    yv = (collide_x[3].pos[1] - self.pos[1]) / self.h
                    if yv > -0.25 and yv < 0:
                        yv = -0.25
                    elif yv < 0.25 and yv > 0:
                        yv = 0.25
                    if collide_x[3] != coll_obj_s:
                        collide_x[3].move(speed * 0.5, math.atan2(yv, dx))
            self.pos[1] += dy
            collide_y = self.collide(0, (dy < 0)*2-1)
            if collide_y[0]:
                coll = 1
                if dy > 0.01:
                    self.pos[1] = collide_y[2] - self.h/2
                elif dy < 0.01:
                    self.pos[1] = collide_y[2] + self.h/2
                #
                if collide_y[3] != None and collide_y[3]._class == "unit" and self._class == "unit":
                    xv = (collide_y[3].pos[0] - self.pos[0]) / self.w
                    if xv > -0.25 and xv < 0:
                        xv = -0.25
                    elif xv < 0.25 and xv > 0:
                        xv = 0.25
                    if collide_y[3] != coll_obj_s:
                        collide_y[3].move(speed * 0.5, math.atan2(dy, xv))
        else:
            coll = 1
        #
        return(coll, coll_obj_s, coll_obj_x, coll_obj_y)

    def collide(self, spx, spy):#spx, spy: 1 - движется влево, 0 - не движется, -1 - движется вправо
        """
        возвращает:
        было ли столкновение
        координата x, на которой произошло столкновение
        координата y, на которой произошло столкновение
        объект, с которым столкнулись
        """
        if self.pos[0] < self.w/2 or self.pos[1] < self.h/2:#со стенами
            return(1, 0, 0, None, "wl")
        if self.pos[0] > self.world.w * 16 - self.w/2 or self.pos[1] > self.world.h * 16 - self.h/2:
            return(1, self.world.w * 16, self.world.h * 16, None, "wl")
        #
        count = [max(math.ceil(self.w / 16), 2), max(math.ceil(self.h / 16), 2)]#с блоками
        centpos = [int(self.pos[0] // 16), int(self.pos[1] // 16)]
        for x in range(int(centpos[0] - count[0] / 2), int(centpos[0] + count[0] / 2) + 1, 1):
            for y in range(int(centpos[1] - count[1] / 2), int(centpos[1] + count[1] / 2) + 1, 1):
                if self.world.test_for_block_pos((x, y)):
                    if self.world.field[x][y].has_hitbox and self.collide_block(x * 16, y * 16):
                        return(1, x * 16 + 16 * (spx/2+0.5), y * 16 + 16 * (spy/2+0.5), self.world.field[x][y], "bl")
        #
        lobj = None
        lpos = 0
        if spx == 1 or spy == 1:
            lpos = -9999
        elif spx == -1 or spy == -1:
            lpos = 99999999999
        if self._class != "bullet":
            for obj in self.world.objects:#с другими юнитами
                if self.entity_collide(obj) and obj._class != "bullet":
                    if self._class == "unit" and obj._class == "unit":
                        if self.player == obj.player:
                            if obj.command == self.command and self.command != None:
                                if obj.stop_flag and (self.pos[0] - self.command[0][0]) ** 2 + (self.pos[1] - self.command[0][1]) ** 2 < 49:
                                    self.stop_flag = 1
                                    self.path = []
                            if obj.inv_flag != 0 and obj.command != None:
                                continue
                    if spx == 0 and spy == 0 and self not in self.player.selected_units:
                        pass
                    if spx == 0 and spy == 0:
                        return(1, obj.pos[0] + obj.w / 2 * spx, obj.pos[1] + obj.h / 2 * spy, obj, "sp=0")
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
            return(1, lobj.pos[0] + lobj.w / 2 * spx, lobj.pos[1] + lobj.h / 2 * spy, lobj, "sp!=0")
        return(0, 0, 0, None, "no")

    def collide_block(self, bl_x, bl_y):
        if (abs(self.pos[0] - (bl_x + 8)) < self.w/2 + 8 and abs(self.pos[1] - (bl_y + 8)) < self.h/2 + 8 and
                abs(abs(self.pos[0] - (bl_x + 8)) - (self.w/2 + 8)) > 0.01 and abs(abs(self.pos[1] - (bl_y + 8)) - (self.h/2 + 8)) > 0.01):
            return(1)
        return(0)

    def entity_collide(self, obj):
        if obj != self:
            if (abs(self.pos[0] - obj.pos[0]) < self.w/2 + obj.w/2 and abs(self.pos[1] - obj.pos[1]) < self.h/2 + obj.h/2 and
                    abs(abs(self.pos[0] - obj.pos[0]) - (self.w/2 + obj.w/2)) > 0.01 and abs(abs(self.pos[1] - obj.pos[1]) - (self.h/2 + obj.h/2)) > 0.01):
                return(1)
        return(0)