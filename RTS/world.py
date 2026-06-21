from farmgui import *
from blocks import *
from chunk import *
from random import randint as rand
from units import *
import opensimplex
import math
from players import *

class World(Panel):
    def __init__(self, w=5, h=5):
        Panel.__init__(self, (0, 0, 1920, 1080))
        self.ch_w = w
        self.ch_h = h
        self.w = w * 16
        self.h = h * 16
        self.zoom = 3
        self.min_zoom = 1
        self.max_zoom = 6
        self.cam_pos = [w * 256 / 2, h * 256 / 2]#позиция центра камеры
        self.cam_speed = 5
        self.display_W = pygame.display.Info().current_w
        self.display_H = pygame.display.Info().current_h
        self.zoom_timer = 0
        self.zoom_speed = 0
        self.pause = 0
        #
        self.draw_path = 0
        self.draw_corners = 0
        #
        self.objects = []
        self.players = [UserPlayer(self), AiPlayer(self)]
        self.player = self.players[0]#игрок - пользователь
        #
        self.action_type = None
        self.action_pos = [0, 0]
        #
        self.field = [[None for y in range(self.w)] for x in range(self.h)]
        self.field = [[Air(self, (x, y)) for y in range(self.h)] for x in range(self.w)]
        self.unit_field = [[[] for y in range(self.w)] for x in range(self.h)]
        opensimplex.seed(rand(0, 999999999999))
        '''for x in range(self.w):
            for y in range(self.h):
                if opensimplex.noise2(x / 10, y / 10) > 0:
                    Stone(self, (x, y))'''
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
        if self.zoom_timer % 2 == 0:
            self.zoom += self.zoom_speed * 2
        if self.zoom_timer > 0:
            self.zoom_timer -= 1
        #
        if pygame.mouse.get_pressed()[0]:#установка
            blockpos = [
                int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
            ]
            if self.test_for_block_pos(blockpos):
                self.field[blockpos[0]][blockpos[1]] = Stone(self, blockpos)
                self.chunks[blockpos[0] // 16][blockpos[1] // 16].update_image()
        #
        if pygame.mouse.get_pressed()[2]:#ломание
            blockpos = [
                int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
            ]
            if self.test_for_block_pos(blockpos):
                self.field[blockpos[0]][blockpos[1]] = Air(self, blockpos)
                self.chunks[blockpos[0] // 16][blockpos[1] // 16].update_image()
        #
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.objects.append(Unit(self, self.player, self.display_to_game(mousepos), 30, 30))
                if event.key == pygame.K_2:
                    for obj in self.objects:
                        if obj._class == "unit":
                            pos = self.display_to_game(mousepos)
                            if pos[0] > obj.pos[0] - obj.w/2 and pos[0] < obj.pos[0] + obj.w/2 and pos[1] > obj.pos[1] - obj.h/2 and pos[1] < obj.pos[1] + obj.h/2:
                                obj.kill()
                if event.key == pygame.K_F1:
                    self.draw_path = not self.draw_path
                if event.key == pygame.K_F2:
                    self.draw_corners = not self.draw_corners
                if event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
                if event.key == pygame.K_f and self.action_type == None:
                    self.action_pos = self.display_to_game(mousepos)
                    self.action_type = "units"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f and self.action_type == "units":
                    self.action_type = None
                    self.player.selected_units = []
                    for obj in self.objects:
                        if obj._class == "unit" and obj.player == self.player:
                            pos = self.display_to_game(mousepos)
                            corn_pos = [#позиция левого верхнего угла выделения
                                pos[0] if self.action_pos[0] - pos[0] >= 0 else self.action_pos[0],
                                pos[1] if self.action_pos[1] - pos[1] >= 0 else self.action_pos[1]
                            ]
                            corn_pos2 = [#позиция правого нижнего угла выделения
                                pos[0] if self.action_pos[0] - pos[0] < 0 else self.action_pos[0],
                                pos[1] if self.action_pos[1] - pos[1] < 0 else self.action_pos[1]
                            ]
                            if obj.pos[0] > corn_pos[0] - obj.w/2 and obj.pos[0] < corn_pos2[0] + obj.w/2 and \
                                    obj.pos[1] > corn_pos[1] - obj.h/2 and obj.pos[1] < corn_pos2[1] + obj.h/2:
                                self.player.selected_units.append(obj)
        #
        #ДЕЙСТВИЯ ИГРОКА
        #
        if self.action_type == "units":
            pass
        #
        #ОБНОВЛЕНИЕ
        #
        if not self.pause:
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
        for x in range(int(self.cam_pos[0] / 256 - count[0] / 2), int(self.cam_pos[0] / 256 + count[0] / 2) + 1):
            for y in range(int(self.cam_pos[1] / 256 - count[1] / 2), int(self.cam_pos[1] / 256 + count[1] / 2) + 1):
                if x >= 0 and x < self.ch_w and y >= 0 and y < self.ch_h:
                    screen.blit(self.chunks[x][y].scaled_fog_image, self.game_to_display((x * 256, y * 256)))
        #
        if self.action_type != None:
            pos = self.game_to_display(self.action_pos)
            img = pygame.Surface((abs(mousepos[0] - pos[0]), abs(mousepos[1] - pos[1])), pygame.SRCALPHA)
            if self.action_type == "units":
                img.fill((255, 128, 0, 128))
            screen.blit(img, (pos[0] if mousepos[0] - pos[0] >= 0 else mousepos[0],
                              pos[1] if mousepos[1] - pos[1] >= 0 else mousepos[1]))
        #
        utils.render_text(str(self.zoom), (0, 25), screen, color=(255, 0, 0))
        utils.render_text(str(d), (0, 50), screen, color=(255, 0, 0))
        utils.render_text(str(self.cam_pos), (0, 75), screen, color=(255, 0, 0))
        utils.render_text("pause: " + str(self.pause), (0, 100), screen, color=(255, 0, 0))
        utils.render_text("draw path: " + str(self.draw_path), (0, 125), screen, color=(255, 0, 0))
        utils.render_text("draw corners: " + str(self.draw_corners), (0, 150), screen, color=(255, 0, 0))

    def display_to_game(self, disp_pos):#перевод экранных координат в игровые
        pos = [
            (self.cam_pos[0] * self.zoom - self.display_W / 2 + disp_pos[0]) / self.zoom,
            (self.cam_pos[1] * self.zoom - self.display_H / 2 + disp_pos[1]) / self.zoom
        ]
        return(pos)

    def game_to_display(self, game_pos):#перевод игровых координат в экранные
        pos = [
            round((game_pos[0] - self.cam_pos[0]) * self.zoom + self.display_W / 2),
            round((game_pos[1] - self.cam_pos[1]) * self.zoom + self.display_H / 2)
        ]
        return(pos)

    def test_for_block_pos(self, pos):
        return(pos[0] >= 0 and pos[0] < self.w and pos[1] >= 0 and pos[1] < self.h)

    def test_for_pos(self, pos):
        return(pos[0] >= 0 and pos[0] < self.w * 16 and pos[1] >= 0 and pos[1] < self.h * 16)