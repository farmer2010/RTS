import pygame
from farmgui import *
from blocks import *
from chunk import *
from random import randint as rand
from units import *
import opensimplex
import math
from players import *

W = pygame.display.Info().current_w
H = pygame.display.Info().current_h

class World(Panel):
    def __init__(self, w=5, h=5):
        Panel.__init__(self, (0, 0, W, H))
        self.ch_w = w
        self.ch_h = h
        self.w = w * 16
        self.h = h * 16
        self.zoom = 3
        self.min_zoom = 1
        self.max_zoom = 6
        self.cam_pos = [w * 256 / 2, h * 256 / 2]#позиция центра камеры
        self.cam_speed = 10
        self.display_W = W
        self.display_H = H
        self.zoom_timer = 0
        self.zoom_speed = 0
        self.pause = 0
        self.command_index = 0
        self.set_rotate = 0
        self.steps = 0
        self.phase = 0
        #
        self.draw_path = 0
        self.draw_command = 0
        self.draw_path_index = 0
        self.draw_pos = 0
        self.air_generator = Air
        #
        self.objects = []
        self.players = [UserPlayer(self), AiPlayer(self)]
        self.player = self.players[0]#игрок - пользователь
        self.items = []
        #
        self.action_type = None
        self.action_pos = [0, 0]
        #
        self.field = [[Air(self, (x, y)) for y in range(self.h)] for x in range(self.w)]
        self.ground_field = [[Air(self, (x, y)) for y in range(self.h)] for x in range(self.w)]
        self.unit_field = [[[] for y in range(self.w)] for x in range(self.h)]
        opensimplex.seed(rand(0, 999999999999))
        for x in range(self.w):
            for y in range(self.h):
                f = opensimplex.noise2(x / 30, y / 30)
                self.ground_field[x][y] = Grass(self, (x, y))
                if f > 0.5:
                    self.field[x][y] = Stone(self, (x, y))
                elif f > -0.1:
                    self.field[x][y] = Air(self, (x, y))
                elif f > -0.25:
                    self.field[x][y] = Air(self, (x, y))
                    self.ground_field[x][y] = Sand(self, (x, y))
                else:
                    self.field[x][y] = Water(self, (x, y))
                #self.field[x][y] = Conveyor(self, (x, y))
        self.chunks = [[Chunk(self, (x, y)) for y in range(self.ch_w)] for x in range(self.ch_h)]
        #
        self.add(Panel((0, 0, 100, 100)))

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
        if pygame.mouse.get_pressed()[0] and not keys[pygame.K_LSHIFT]:#установка
            blockpos = [
                int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
            ]
            if self.test_for_block_pos(blockpos):
                if self.field[blockpos[0]][blockpos[1]].type == "air":
                    self.field[blockpos[0]][blockpos[1]] = Conveyor(self, blockpos, rotate=self.set_rotate)
                    self.chunks[blockpos[0] // 16][blockpos[1] // 16].update_image()
        #
        if pygame.mouse.get_pressed()[2]:#ломание
            self.action_type = None
            blockpos = [
                int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
            ]
            if self.test_for_block_pos(blockpos):
                if self.field[blockpos[0]][blockpos[1]].type != "air":
                    self.field[blockpos[0]][blockpos[1]].remove_block()
        #
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.objects.append(Tank(self, self.player, self.display_to_game(mousepos)))
                if event.key == pygame.K_2:
                    self.objects.append(Worker(self, self.player, self.display_to_game(mousepos)))
                if event.key == pygame.K_3:
                    for obj in self.objects:
                        if obj._class == "unit":
                            pos = self.display_to_game(mousepos)
                            if pos[0] > obj.pos[0] - obj.w/2 and pos[0] < obj.pos[0] + obj.w/2 and pos[1] > obj.pos[1] - obj.h/2 and pos[1] < obj.pos[1] + obj.h/2:
                                obj.kill()
                if event.key == pygame.K_4:
                    blockpos = [
                        int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                        int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
                    ]
                    if self.test_for_block_pos(blockpos):
                        if self.field[blockpos[0]][blockpos[1]].type == "conveyor":
                            itm = [blockpos, "stone", self.field[blockpos[0]][blockpos[1]]]
                            if self.field[blockpos[0]][blockpos[1]].set_item(itm):
                                self.items.append(itm)
                if event.key == pygame.K_5:
                    blockpos = [
                        int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                        int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
                    ]
                    if self.test_for_block_pos(blockpos):
                        if self.field[blockpos[0]][blockpos[1]].type == "conveyor":
                            itm = [blockpos, "coal", self.field[blockpos[0]][blockpos[1]]]
                            if self.field[blockpos[0]][blockpos[1]].set_item(itm):
                                self.items.append(itm)
                if event.key == pygame.K_6:
                    blockpos = [
                        int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                        int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
                    ]
                    if self.test_for_block_pos(blockpos):
                        if self.field[blockpos[0]][blockpos[1]].type == "conveyor":
                            if self.field[blockpos[0]][blockpos[1]].item1 != None:
                                self.items.remove(self.field[blockpos[0]][blockpos[1]].item1)
                                self.field[blockpos[0]][blockpos[1]].item1 = None
                            if self.field[blockpos[0]][blockpos[1]].item2 != None:
                                self.items.remove(self.field[blockpos[0]][blockpos[1]].item2)
                                self.field[blockpos[0]][blockpos[1]].item2 = None
                if event.key == pygame.K_F1:
                    self.draw_path = not self.draw_path
                if event.key == pygame.K_F2:
                    self.draw_command = not self.draw_command
                if event.key == pygame.K_F3:
                    self.draw_path_index = not self.draw_path_index
                if event.key == pygame.K_F4:
                    self.draw_pos = not self.draw_pos
                if event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
                if self.action_type == None:
                    if event.key == pygame.K_f:
                        self.action_pos = self.display_to_game(mousepos)
                        self.action_type = "units"
                    if event.key == pygame.K_g:
                        self.action_pos = self.display_to_game(mousepos)
                        self.action_type = "dig"
                    if event.key == pygame.K_c:
                        self.action_pos = self.display_to_game(mousepos)
                        self.action_type = "clear"
                if event.key == pygame.K_r:
                    self.set_rotate = (self.set_rotate + 1) % 4
            #
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f and self.action_type == "units":
                    self.action_func()
                if event.key == pygame.K_g and self.action_type == "dig":
                    self.action_func()
                if event.key == pygame.K_c and self.action_type == "clear":
                    self.action_func()
            #
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and keys[pygame.K_LSHIFT]:
                    for obj in self.objects:
                        if obj._class == "unit" and obj.player == self.player and obj in self.player.selected_units:
                            mousepos = pygame.mouse.get_pos()
                            pos = [
                                int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) / self.zoom / 16),
                                int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) / self.zoom / 16)
                            ]
                            obj.move_command(pos)
                    self.command_index += 1
        #
        #ОБНОВЛЕНИЕ
        #
        if not self.pause:
            for obj in self.objects:
                obj.update(events)
            if self.steps % 6 == 0:
                for item in self.items:
                    pos = item[0]
                    if self.field[item[2].pos[0]][item[2].pos[1]].type == "conveyor":
                        self.field[item[2].pos[0]][item[2].pos[1]].move_item()
                self.phase = (self.phase + 1) % 2
            self.steps += 1
        #
        for x in range(self.ch_w):
            for y in range(self.ch_h):
                if self.chunks[x][y].image_changes:
                    self.chunks[x][y].update_image()
                    self.chunks[x][y].image_changes = False
        #
        for x in range(self.ch_w):
            for y in range(self.ch_h):
                if self.chunks[x][y].fog_changes:
                    self.chunks[x][y].update_fog_image()
                    self.chunks[x][y].fog_changes = False
        #

    def action_func(self):
        mousepos = pygame.mouse.get_pos()
        pos = self.display_to_game(mousepos)
        corn_pos = [  # позиция левого верхнего угла выделения
            pos[0] if self.action_pos[0] - pos[0] >= 0 else self.action_pos[0],
            pos[1] if self.action_pos[1] - pos[1] >= 0 else self.action_pos[1]
        ]
        corn_pos2 = [  # позиция правого нижнего угла выделения
            pos[0] if self.action_pos[0] - pos[0] < 0 else self.action_pos[0],
            pos[1] if self.action_pos[1] - pos[1] < 0 else self.action_pos[1]
        ]
        #
        bl_corn_pos = [  # позиция левого верхнего угла выделения
            int(corn_pos[0] // 16),
            int(corn_pos[1] // 16)
        ]
        bl_corn_pos2 = [  # позиция правого нижнего угла выделения
            int(corn_pos2[0] // 16),
            int(corn_pos2[1] // 16)
        ]
        #
        if self.action_type == "units":
            self.player.selected_units = []
            for obj in self.objects:
                if obj._class == "unit" and obj.player == self.player:
                    if obj.pos[0] > corn_pos[0] - obj.w / 2 and obj.pos[0] < corn_pos2[0] + obj.w / 2 and \
                            obj.pos[1] > corn_pos[1] - obj.h / 2 and obj.pos[1] < corn_pos2[1] + obj.h / 2:
                        self.player.selected_units.append(obj)
        #
        for x in range(bl_corn_pos[0], bl_corn_pos2[0] + 1):
            for y in range(bl_corn_pos[1], bl_corn_pos2[1] + 1):
                if self.test_for_block_pos((x, y)) and self.field[x][y].can_mined:
                    if self.action_type == "dig":
                        self.player.task_field[x][y] = 1
                    elif self.action_type == "clear":
                        self.player.task_field[x][y] = 0
        #
        if self.action_type == "clear" or self.action_type == "dig":
            for x in range(int(bl_corn_pos[0] // 16), int(bl_corn_pos2[0] // 16 + 1)):
                for y in range(int(bl_corn_pos[1] // 16), int(bl_corn_pos2[1] // 16 + 1)):
                    if x >= 0 and x < self.ch_w and y >= 0 and y < self.ch_h:
                        self.chunks[x][y].update_image()
                        #pygame.draw.rect(self.chunks[x][y].scaled_image, (0, 0, 0), (0, 0, 100, 100))
        #
        self.action_type = None

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
        for item in self.items:
            pos = item[0]
            '''if self.field[pos[0]][pos[1]].type == "conveyor":
                if self.field[pos[0]][pos[1]].item1 != None:
                    img = pygame.transform.scale(items[self.field[pos[0]][pos[1]].item1[1]], (16 * self.zoom, 16 * self.zoom))
                    screen.blit(img, self.game_to_display([pos[0] * 16, pos[1] * 16]))
                if self.field[pos[0]][pos[1]].item2 != None:
                    img = pygame.transform.scale(items[self.field[pos[0]][pos[1]].item2[1]], (16 * self.zoom, 16 * self.zoom))
                    screen.blit(img, self.game_to_display([pos[0] * 16, pos[1] * 16]))'''
            img = pygame.transform.scale(items[item[1]], (16 * self.zoom, 16 * self.zoom))
            screen.blit(img, self.game_to_display([pos[0] * 16, pos[1] * 16]))
            screen.blit(pygame.transform.scale(dig_img, (16 * self.zoom, 16 * self.zoom)), self.game_to_display([item[2].pos[0] * 16, item[2].pos[1] * 16]))
        #
        for obj in self.objects:
            obj.draw(screen)
        #
        '''for x in range(int(self.cam_pos[0] / 256 - count[0] / 2), int(self.cam_pos[0] / 256 + count[0] / 2) + 1):
            for y in range(int(self.cam_pos[1] / 256 - count[1] / 2), int(self.cam_pos[1] / 256 + count[1] / 2) + 1):
                if x >= 0 and x < self.ch_w and y >= 0 and y < self.ch_h:
                    screen.blit(self.chunks[x][y].scaled_fog_image, self.game_to_display((x * 256, y * 256)))'''
        #
        if self.action_type != None:
            pos = self.game_to_display(self.action_pos)
            mpos = self.display_to_game(mousepos)
            img = pygame.Surface((abs(mousepos[0] - pos[0]), abs(mousepos[1] - pos[1])), pygame.SRCALPHA)
            if self.action_type == "clear" or self.action_type == "dig":
                corn_pos = [  # позиция левого верхнего угла выделения
                    min(mpos[0], self.action_pos[0]) // 16 * 16,
                    min(mpos[1], self.action_pos[1]) // 16 * 16
                ]
                corn_pos2 = [  # позиция правого нижнего угла выделения
                    max(mpos[0], self.action_pos[0]) // 16 * 16 + 16,
                    max(mpos[1], self.action_pos[1]) // 16 * 16 + 16
                ]
                d_corn_pos = self.game_to_display(corn_pos)
                d_corn_pos2 = self.game_to_display(corn_pos2)
                img = pygame.Surface((abs(d_corn_pos[0] - d_corn_pos2[0]), abs(d_corn_pos[1] - d_corn_pos2[1])), pygame.SRCALPHA)
            #
            if self.action_type == "units":
                img.fill((255, 128, 0, 128))
            elif self.action_type == "dig":
                img.fill((255, 0, 0, 100))
            elif self.action_type == "clear":
                img.fill((0, 100, 255, 100))
            #
            if self.action_type == "units":
                screen.blit(img, (min(pos[0], mousepos[0]),
                                  min(pos[1], mousepos[1])))
            elif self.action_type == "clear" or self.action_type == "dig":
                corn_pos = self.game_to_display([min(mpos[0], self.action_pos[0]) // 16 * 16, min(mpos[1], self.action_pos[1]) // 16 * 16])
                screen.blit(img, (min(pos[0], corn_pos[0]),
                                  min(pos[1], corn_pos[1])))
        #
        utils.render_text(str(self.zoom), (0, 25), screen, color=(255, 0, 0))
        utils.render_text(str(d), (0, 50), screen, color=(255, 0, 0))
        utils.render_text(str(self.cam_pos), (0, 75), screen, color=(255, 0, 0))
        utils.render_text("pause: " + str(self.pause), (0, 100), screen, color=(255, 0, 0))
        utils.render_text("draw path: " + str(self.draw_path), (0, 125), screen, color=(255, 0, 0))
        utils.render_text("draw command: " + str(self.draw_command), (0, 150), screen, color=(255, 0, 0))
        utils.render_text("draw path index: " + str(self.draw_path_index), (0, 175), screen, color=(255, 0, 0))
        utils.render_text("draw pos: " + str(self.draw_pos), (0, 200), screen, color=(255, 0, 0))
        if self.draw_pos:
            blockpos = [
                int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
            ]
            utils.render_text(str(blockpos), mousepos, screen, color=(255, 0, 0))

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