import pygame
from entity import *

class Projectile(Entity):
    def __init__(self, world, player, pos, w, h, rotate, speed, distance, damage):
        Entity.__init__(self, world, player, "bullet", pos, w, h)
        self.world = world
        self.pos = pos
        self.w = w
        self.h = h
        self.rotate = rotate
        self.speed = speed
        self.max_distance = distance
        self.damage = damage
        self.distance = 0
        self.image.fill((0, 0, 255))

    def update(self, events):
        self.move(self.speed, self.rotate)
        self.distance += self.speed
        if self.distance >= self.max_distance:
            self.kill()

    def move(self, speed, rotate):
        collide = self.collide(0, 0)
        if not collide[0]:
            dx = math.cos(rotate) * speed
            dy = math.sin(rotate) * speed
            self.pos[0] += dx
            self.pos[1] += dy
        else:
            if collide[1] != None and collide[1]._class == "unit":
                collide[1].health -= self.damage
                if collide[1].health <= 0:
                    collide[1].kill()
            self.kill()

    def collide(self, spx=0, spy=0):
        """
        возвращает:
        было ли столкновение
        объект, с которым столкнулись
        """
        if self.pos[0] < self.w/2 or self.pos[1] < self.h/2:#со стенами
            return(1, None)
        if self.pos[0] > self.world.w * 16 - self.w/2 or self.pos[1] > self.world.h * 16 - self.h/2:
            return(1, None)
        #
        count = [max(math.ceil(self.w / 16), 2), max(math.ceil(self.h / 16), 2)]#с блоками
        centpos = [int(self.pos[0] // 16), int(self.pos[1] // 16)]
        for x in range(int(centpos[0] - count[0] / 2), int(centpos[0] + count[0] / 2) + 1, 1):
            for y in range(int(centpos[1] - count[1] / 2), int(centpos[1] + count[1] / 2) + 1, 1):
                if self.world.test_for_block_pos((x, y)):
                    if self.world.field[x][y].has_hitbox and self.collide_block(x * 16, y * 16):
                        return(1, self.world.field[x][y])
        #
        for obj in self.world.objects:#с другими юнитами
            if self.entity_collide(obj) and obj._class == "unit":
                if self.player != obj.player:
                    return(1, obj)
        return(0, None)