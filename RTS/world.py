from farmgui import *
from blocks import *
from chunk import *
from random import randint as rand
from units import *
import opensimplex
import math

class World(Panel):
    def __init__(self, w=13, h=13):
        Panel.__init__(self, (0, 0, 1920, 1080))
        self.ch_w = w
        self.ch_h = h
        self.w = w * 16
        self.h = h * 16
        self.zoom = 3
        self.min_zoom = 1
        self.max_zoom = 10
        self.cam_pos = [0, 0]#позиция центра камеры
        self.cam_speed = 5
        self.display_W = pygame.display.Info().current_w
        self.display_H = pygame.display.Info().current_h
        self.zoom_timer = 0
        self.zoom_speed = 0
        #
        self.objects = []
        #
        self.field = [[None for y in range(self.w)] for x in range(self.h)]
        self.field = [[Air(self, (x, y)) for y in range(self.h)] for x in range(self.w)]
        opensimplex.seed(rand(0, 999999999999))
        for x in range(self.w):
            for y in range(self.h):
                if opensimplex.noise2(x / 10, y / 10) > 0:
                    Stone(self, (x, y))
        self.chunks = [[Chunk(self, (x, y)) for y in range(self.ch_w)] for x in range(self.ch_h)]

    def update(self, events):
        #
        #УПРАВЛЕНИЕ
        #
        keys = pygame.key.get_pressed()
        move_keys = [
            keys[pygame.K_w],
            keys[pygame.K_d],
            keys[pygame.K_s],
            keys[pygame.K_a]
        ]
        if sum(move_keys) > 0:
            if move_keys[1] + move_keys[3] == 0:
                if move_keys[0]:
                    self.cam_pos[1] -= self.cam_speed
                elif move_keys[2]:
                    self.cam_pos[1] += self.cam_speed
            elif move_keys[0] + move_keys[2] == 0:
                if move_keys[3]:
                    self.cam_pos[0] -= self.cam_speed
                elif move_keys[1]:
                    self.cam_pos[0] += self.cam_speed
            else:
                if move_keys[0]:
                    if move_keys[3]:
                        self.cam_pos[0] -= self.cam_speed / 1.4
                        self.cam_pos[1] -= self.cam_speed / 1.4
                    elif move_keys[1]:
                        self.cam_pos[0] += self.cam_speed / 1.4
                        self.cam_pos[1] -= self.cam_speed / 1.4
                elif move_keys[2]:
                    if move_keys[3]:
                        self.cam_pos[0] -= self.cam_speed / 1.4
                        self.cam_pos[1] += self.cam_speed / 1.4
                    elif move_keys[1]:
                        self.cam_pos[0] += self.cam_speed / 1.4
                        self.cam_pos[1] += self.cam_speed / 1.4
        #
        if self.zoom_timer == 0:
            self.zoom = round(self.zoom)
            self.zoom_speed = 0
            wheel = self.input_manager.get_mousewheel()
            if wheel != 0:
                self.zoom_timer = 20
                self.zoom_speed = (max(min(self.zoom + wheel, self.max_zoom), self.min_zoom) - self.zoom) / 20
        self.zoom += self.zoom_speed
        if self.zoom_timer > 0:
            self.zoom_timer -= 1
        #
        #УСТАНОВКА/ЛОМАНИЕ
        #
        mousepos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:#установка
            blockpos = [
                int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
            ]
            if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h:
                self.field[blockpos[0]][blockpos[1]] = Stone(self, blockpos)
                self.chunks[blockpos[0] // 16][blockpos[1] // 16].update_image()
        #
        if pygame.mouse.get_pressed()[2]:#ломание
            blockpos = [
                int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
            ]
            if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h:
                self.field[blockpos[0]][blockpos[1]] = Air(self, blockpos)
                self.chunks[blockpos[0] // 16][blockpos[1] // 16].update_image()
        #
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    pos = [
                        (self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) / self.zoom,
                        (self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) / self.zoom
                    ]
                    self.objects.append(Unit(self, pos, 30, 30))
        #
        #ОБНОВЛЕНИЕ
        #
        for obj in self.objects:
            obj.update(events)
        #

    def draw(self, screen):
        screen.fill((0, 0, 0))
        d = 0
        count = [math.ceil(self.display_W / (self.zoom * 256)), math.ceil(self.display_H / (self.zoom * 256))]#количество видимых чанков
        for x in range(int(self.cam_pos[0] / 256 - count[0] / 2), int(self.cam_pos[0] / 256 + count[0] / 2) + 1):
            for y in range(int(self.cam_pos[1] / 256 - count[1] / 2), int(self.cam_pos[1] / 256 + count[1] / 2) + 1):
                if x >= 0 and x < self.ch_w and y >= 0 and y < self.ch_h:
                    self.chunks[x][y].draw(screen)
                    d += 1
        #
        for obj in self.objects:
            obj.draw(screen)
        #
        utils.render_text(str(self.zoom), (0, 25), screen, color=(255, 0, 0))
        utils.render_text(str(d), (0, 50), screen, color=(255, 0, 0))
        utils.render_text(str(self.cam_pos), (0, 75), screen, color=(255, 0, 0))