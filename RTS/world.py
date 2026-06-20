from farmgui import *
from blocks import *
from chunk import *
from random import randint as rand
from units import *
import opensimplex
import math
from players import *

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
        self.players = [UserPlayer(self), AiPlayer(self)]
        self.selfplayer = self.players[0]#игрок - пользователь
        #
        self.action_type = None
        self.action_pos = [0, 0]
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
        keys = pygame.key.get_pressed()
        mousepos = pygame.mouse.get_pos()
        #
        #УПРАВЛЕНИЕ
        #
        move_keys = [#перемещение камеры
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
        if self.zoom_timer == 0:#зум
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pos = [
                        (self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) / self.zoom,
                        (self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) / self.zoom
                    ]
                    self.objects.append(Unit(self, self.selfplayer, pos, 30, 30))
                if event.key == pygame.K_f:
                    self.action_pos = [
                        (self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) / self.zoom,
                        (self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) / self.zoom
                    ]
                    self.action_type = "units"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    self.action_type = None
        #
        #ДЕЙСТВИЯ ИГРОКА
        #
        if self.action_type == "units":
            pass
        #
        #ОБНОВЛЕНИЕ
        #
        for obj in self.objects:
            obj.update(events)
        #

    def draw(self, screen):
        mousepos = pygame.mouse.get_pos()
        #
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
        if self.action_type != None:
            pos = [
                round((self.action_pos[0] - self.cam_pos[0]) * self.zoom + self.display_W / 2),
                round((self.action_pos[1] - self.cam_pos[1]) * self.zoom + self.display_H / 2)
            ]
            img = pygame.Surface((abs(mousepos[0] - pos[0]), abs(mousepos[1] - pos[1])), pygame.SRCALPHA)
            if self.action_type == "units":
                img.fill((255, 128, 0, 128))
            screen.blit(img, (pos[0] if mousepos[0] - pos[0] >= 0 else mousepos[0],
                              pos[1] if mousepos[1] - pos[1] >= 0 else mousepos[1]))
        #
        utils.render_text(str(self.zoom), (0, 25), screen, color=(255, 0, 0))
        utils.render_text(str(d), (0, 50), screen, color=(255, 0, 0))
        utils.render_text(str(self.cam_pos), (0, 75), screen, color=(255, 0, 0))
        utils.render_text(str(self.action_pos), (0, 100), screen, color=(255, 0, 0))