import pygame
from farmgui import *
from blocks import *
from chunk import *
from random import randint as rand
from units import *
from opensimplex import *
import math
from players import *

W = pygame.display.Info().current_w
H = pygame.display.Info().current_h

font = pygame.font.Font("files/Better VCR 6.1.ttf", 16)

landscape = [#0.029 1.0 1 0.097 0.503 1 0.509 0.065 0.672 0.845 1.067 1.404
    [#octave 1
        0.029,
        1.0
    ],
    [#octave 2
        0.097,
        0.503
    ],
    [#octave 3
        0.509,
        0.065
    ],
    [
        -0.328,#water
        -0.155,#sand water
        0.067,#sand
        0.404#grass
    ]
]
ore = [#0.076 0.45 1 0.163 0.447 1.131 1.243
    [#stone
        [
            0.076,#octave 1
            0.45
        ],
        [
            0.163,#octave 2
            0.447
        ],
        [
            0.131,#vein level
            0.243#cluster level
        ]
    ],#0.064 0.426 1 0.382 0.792 1.28 1.255
    [#coal
        [
            0.064,#octave 1
            0.426
        ],
        [
            0.382,#octave 2
            0.792
        ],
        [
            0.28,#vein level
            0.255#cluster level
        ]
    ],#0.033 0.45 1 0.163 0.447 1.112 1.243
    [#iron
        [
            0.034,#octave 1
            0.45
        ],
        [
            0.163,#octave 2
            0.447
        ],
        [
            0.14,#vein level
            0.243#cluster level
        ]
    ],#0.029 0.752 1 1.0 0.768 1.155 1.48
    [#copper
        [
            0.029,#octave 1
            0.752
        ],
        [
            1.0,#octave 2
            0.768
        ],
        [
            0.155,#vein level
            0.48#cluster level
        ]
    ],
]
ore_id = [
    "stone ore",
    "coal ore",
    "iron ore",
    "copper ore"
]

pages = [
    [
        "conveyor",
        "junction",
        "router",
        "sorter",
        "inverted sorter",
        "overflow gate",
        "underflow gate"
    ],
    [
        "drill"
    ],
    [
        "iron furnace",
        "copper furnace"
    ],
    [
        "stone turret",
        "stone wall",
        "iron wall"
    ],
    [

    ]
]

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
        self.steps = 0
        self.menu = "game"
        #
        self.map_zoom = 4
        self.map_pos = [self.w/2, self.h/2]
        self.map_speed = 3
        #
        self.draw_path = 0
        self.draw_command = 0
        self.draw_path_index = 0
        self.draw_pos = 0
        self.air_generator = Air
        self.pl_ind = 0
        #
        self.objects = []
        self.players = [UserPlayer(self), AiPlayer(self)]
        self.player = self.players[0]#игрок - пользователь
        self.items = []
        #
        self.page_index = 0
        self.select_rotate = 0
        self.select_block = None
        #
        self.action_type = None
        self.action_pos = [0, 0]
        #
        self.minimap = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.minimap_background = get_text_box_image(self.w + 18, self.h + 18, (90, 90, 90))
        self.fog_minimap = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.fog_minimap.fill((0, 0, 0))
        self.field = [[Air(self, (x, y)) for y in range(self.h)] for x in range(self.w)]
        self.ground_field = [[Air(self, (x, y)) for y in range(self.h)] for x in range(self.w)]
        self.ore_field = [[None for y in range(self.h)] for x in range(self.w)]
        self.unit_field = [[[] for y in range(self.w)] for x in range(self.h)]
        land_oct1 = OpenSimplex(seed=rand(-9999999999, 9999999999))
        land_oct2 = OpenSimplex(seed=rand(-9999999999, 9999999999))
        land_oct3 = OpenSimplex(seed=rand(-9999999999, 9999999999))
        stone_oct1 = OpenSimplex(seed=rand(-9999999999, 9999999999))
        stone_oct2 = OpenSimplex(seed=rand(-9999999999, 9999999999))
        coal_oct1 = OpenSimplex(seed=rand(-9999999999, 9999999999))
        coal_oct2 = OpenSimplex(seed=rand(-9999999999, 9999999999))
        iron_oct1 = OpenSimplex(seed=rand(-9999999999, 9999999999))
        iron_oct2 = OpenSimplex(seed=rand(-9999999999, 9999999999))
        copper_oct1 = OpenSimplex(seed=rand(-9999999999, 9999999999))
        copper_oct2 = OpenSimplex(seed=rand(-9999999999, 9999999999))
        for x in range(self.w):
            for y in range(self.h):
                noise = land_oct1.noise2(x * landscape[0][0], y * landscape[0][0]) * landscape[0][1]
                noise += land_oct2.noise2(x * landscape[1][0], y * landscape[1][0]) * landscape[1][1]
                noise += land_oct3.noise2(x * landscape[2][0], y * landscape[2][0]) * landscape[2][1]
                if noise < landscape[3][0]:#water
                    self.field[x][y] = Water(self, (x, y))
                    self.ground_field[x][y] = Grass(self, (x, y))
                elif noise < landscape[3][1]:#sand water
                    self.ground_field[x][y] = SandyWater(self, (x, y))
                    self.field[x][y] = Air(self, (x, y))
                elif noise < landscape[3][2]:#sand
                    self.ground_field[x][y] = Sand(self, (x, y))
                    self.field[x][y] = Air(self, (x, y))
                elif noise < landscape[3][3]:#grass
                    self.ground_field[x][y] = Grass(self, (x, y))
                    self.field[x][y] = Air(self, (x, y))
                else:#stone
                    self.ground_field[x][y] = StoneFloor(self, (x, y))
                    self.field[x][y] = Stone(self, (x, y))
                #
                #
                stone_cluster_noise = stone_oct1.noise2(x * ore[0][0][0], y * ore[0][0][0]) * ore[0][0][1]
                stone_vein_noise = stone_oct2.noise2(x * ore[0][1][0], y * ore[0][1][0]) * ore[0][1][1]
                if stone_cluster_noise > ore[0][2][1] and stone_vein_noise > ore[0][2][0]:
                    if self.field[x][y].type == "air" and (self.ground_field[x][y].type == "grass" or self.ground_field[x][y].type == "sand"):
                        self.ore_field[x][y] = ["stone", int(stone_vein_noise * 320)]
                #
                coal_cluster_noise = coal_oct1.noise2(x * ore[1][0][0], y * ore[1][0][0]) * ore[1][0][1]
                coal_vein_noise = coal_oct2.noise2(x * ore[1][1][0], y * ore[1][1][0]) * ore[1][1][1]
                if coal_cluster_noise > ore[1][2][1] and coal_vein_noise > ore[1][2][0]:
                    if self.field[x][y].type == "air" and (self.ground_field[x][y].type == "grass" or self.ground_field[x][y].type == "sand"):
                        self.ore_field[x][y] = ["coal", int(coal_vein_noise * 130)]
                    elif self.field[x][y].type == "stone":
                        self.field[x][y] = Ore(self, (x, y), "coal ore")
                #
                iron_cluster_noise = iron_oct1.noise2(x * ore[2][0][0], y * ore[2][0][0]) * ore[2][0][1]
                iron_vein_noise = iron_oct2.noise2(x * ore[2][1][0], y * ore[2][1][0]) * ore[2][1][1]
                if iron_cluster_noise > ore[2][2][1] and iron_vein_noise > ore[2][2][0]:
                    if self.field[x][y].type == "air" and (self.ground_field[x][y].type == "grass" or self.ground_field[x][y].type == "sand"):
                        self.ore_field[x][y] = ["iron", int(iron_vein_noise * 250)]
                    elif self.field[x][y].type == "stone":
                        self.field[x][y] = Ore(self, (x, y), "iron ore")
                #
                copper_cluster_noise = copper_oct1.noise2(x * ore[3][0][0], y * ore[3][0][0]) * ore[3][0][1]
                copper_vein_noise = copper_oct2.noise2(x * ore[3][1][0], y * ore[3][1][0]) * ore[3][1][1]
                if copper_cluster_noise > ore[3][2][1] and copper_vein_noise > ore[3][2][0]:
                    if self.field[x][y].type == "air" and (self.ground_field[x][y].type == "grass" or self.ground_field[x][y].type == "sand"):
                        self.ore_field[x][y] = ["copper", int(copper_vein_noise * 150)]
                    elif self.field[x][y].type == "stone":
                        self.field[x][y] = Ore(self, (x, y), "copper ore")
                #
                self.update_minimap((x, y))
        self.chunks = [[Chunk(self, (x, y)) for y in range(self.ch_w)] for x in range(self.ch_h)]

    def update(self, events):
        keys = pygame.key.get_pressed()
        mousepos = pygame.mouse.get_pos()
        if self.menu == "game":
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
                    self.zoom_timer = 10
                    self.zoom_speed = (max(min(self.zoom + wheel/abs(wheel), self.max_zoom), self.min_zoom) - self.zoom) / 10
            self.zoom += self.zoom_speed
            if self.zoom_timer > 0:
                self.zoom_timer -= 1
            #
            inv = mousepos[0] >= W - 268 and mousepos[1] >= H - 332
            mnmp = mousepos[0] >= W - self.w - 18 and mousepos[1] <= self.h + 18
            on_ui = inv or mnmp
            #
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.objects.append(Tank(self, self.players[self.pl_ind], self.display_to_game(mousepos)))
                    if event.key == pygame.K_2:
                        self.objects.append(Worker(self, self.players[self.pl_ind], self.display_to_game(mousepos)))
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
                                itm = ["stone", self.field[blockpos[0]][blockpos[1]]]
                                if self.field[blockpos[0]][blockpos[1]].set_item(itm, 0):
                                    self.items.append(itm)
                    if event.key == pygame.K_5:
                        blockpos = [
                            int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                            int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
                        ]
                        if self.test_for_block_pos(blockpos):
                            if self.field[blockpos[0]][blockpos[1]].type == "conveyor":
                                itm = ["coal", self.field[blockpos[0]][blockpos[1]]]
                                if self.field[blockpos[0]][blockpos[1]].set_item(itm, 0):
                                    self.items.append(itm)
                    if event.key == pygame.K_6:
                        blockpos = [
                            int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                            int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
                        ]
                        if self.test_for_block_pos(blockpos):
                            if self.field[blockpos[0]][blockpos[1]].type == "conveyor":
                                self.field[blockpos[0]][blockpos[1]].clear_item()
                    if event.key == pygame.K_7:
                        self.pl_ind = (self.pl_ind + 1) % 2
                    if event.key == pygame.K_F1:
                        self.draw_path = not self.draw_path
                    if event.key == pygame.K_F2:
                        self.draw_command = not self.draw_command
                    if event.key == pygame.K_F3:
                        self.draw_path_index = not self.draw_path_index
                    if event.key == pygame.K_F4:
                        self.draw_pos = not self.draw_pos
                    if event.key == pygame.K_SPACE:
                        self.pause = not self.pause
                    if self.action_type == None:
                        if event.key == pygame.K_f:
                            self.select_block = None
                            self.action_pos = self.display_to_game(mousepos)
                            self.action_type = "units"
                        if event.key == pygame.K_g:
                            self.select_block = None
                            self.action_pos = self.display_to_game(mousepos)
                            self.action_type = "dig"
                        if event.key == pygame.K_c:
                            self.select_block = None
                            self.action_pos = self.display_to_game(mousepos)
                            self.action_type = "clear"
                        if event.key == pygame.K_x:
                            self.select_block = None
                            self.action_pos = self.display_to_game(mousepos)
                            self.action_type = "remove"
                    if event.key == pygame.K_r:
                        self.select_rotate = (self.select_rotate + 1) % 4
                    if event.key == pygame.K_m:
                        self.select_block = None
                        self.menu = "map"
                    if event.key == pygame.K_q:
                        blockpos = [
                            int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                            int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
                        ]
                        if self.test_for_block_pos(blockpos):
                            if self.field[blockpos[0]][blockpos[1]].is_construction:
                                self.select_block = self.field[blockpos[0]][blockpos[1]].type
                            else:
                                self.select_block = None
                #
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_f and self.action_type == "units":
                        self.action_func()
                    if event.key == pygame.K_g and self.action_type == "dig":
                        self.action_func()
                    if event.key == pygame.K_c and self.action_type == "clear":
                        self.action_func()
                    if event.key == pygame.K_x and self.action_type == "remove":
                        self.action_func()
                #
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not on_ui:
                            if keys[pygame.K_LSHIFT]:#команда юнитам
                                pos = [
                                    int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) / self.zoom / 16),
                                    int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) / self.zoom / 16)
                                ]
                                if self.test_for_block_pos(pos):
                                    if self.player.fog[pos[0]][pos[1]] != 0:
                                        for obj in self.player.selected_units:
                                            obj.move_command(pos)
                                        self.command_index += 1
                            else:#нажатие на блок
                                blockpos = [
                                    int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                                    int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
                                ]
                                if self.test_for_block_pos(blockpos):
                                    if self.field[blockpos[0]][blockpos[1]].type != "air":
                                        self.field[blockpos[0]][blockpos[1]].action()
                                        self.chunks[blockpos[0] // 16][blockpos[1] // 16].update_image()
                    if event.button == 3:
                        self.action_type = "remove all"
                        self.select_block = None
                        self.action_pos = self.display_to_game(mousepos)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if inv:
                            self.select_block = None
                            x = (W - mousepos[0]) // 64
                            y = (H - mousepos[1]) // 64
                            if x == 0:
                                self.page_index = min(max(4 - y, 0), 4)
                            elif x > 0:
                                i = -(x - 3) + (4 - y) * 3
                                if i < len(pages[self.page_index]):
                                    self.select_block = pages[self.page_index][i]
                        #
                        if mnmp:
                            self.menu = "map"
                    if event.button == 3 and self.action_type == "remove all":
                        self.action_func()
            #
            if pygame.mouse.get_pressed()[0] and not keys[pygame.K_LSHIFT] and not on_ui:#установка
                blockpos = [
                    int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                    int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
                ]
                if self.test_for_block_pos(blockpos):
                    if self.field[blockpos[0]][blockpos[1]].type == "air":
                        tp = self.select_block if self.select_block != None else "stone"
                        pl = self.players[self.pl_ind] if self.select_block != None else None
                        if keys[pygame.K_KP0]:
                            set_block(self, blockpos, None, "coal ore")
                        elif keys[pygame.K_KP1]:
                            set_block(self, blockpos, None, "iron ore")
                        elif keys[pygame.K_KP2]:
                            set_block(self, blockpos, None, "copper ore")
                        elif keys[pygame.K_KP_DIVIDE]:
                            self.field[blockpos[0]][blockpos[1]] = ItemVacuum(self, blockpos)
                        elif keys[pygame.K_INSERT]:
                            self.ore_field[blockpos[0]][blockpos[1]] = ["stone", 10]
                        elif keys[pygame.K_HOME]:
                            self.ore_field[blockpos[0]][blockpos[1]] = ["coal", 10]
                        elif keys[pygame.K_PAGEUP]:
                            self.ore_field[blockpos[0]][blockpos[1]] = ["iron", 10]
                        elif keys[pygame.K_PAGEDOWN]:
                            self.ore_field[blockpos[0]][blockpos[1]] = ["copper", 10]
                        elif keys[pygame.K_DELETE]:
                            self.ore_field[blockpos[0]][blockpos[1]] = None
                        elif self.select_block != None:
                            #set_block(self, blockpos, pl, tp, rotate=self.select_rotate)
                            self.player.task_field[blockpos[0]][blockpos[1]] = [self.select_block, self.select_rotate]
                        self.chunks[blockpos[0] // 16][blockpos[1] // 16].update_image()
            #
            '''if pygame.mouse.get_pressed()[2] and not on_ui and 0:#ломание
                blockpos = [
                    int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                    int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
                ]
                if self.test_for_block_pos(blockpos):
                    if self.field[blockpos[0]][blockpos[1]].type != "air":
                        self.field[blockpos[0]][blockpos[1]].remove_block()'''
            #
            #ОБНОВЛЕНИЕ
            #
            if not self.pause:
                for obj in self.objects:
                    obj.update(events)
                if self.steps % 6 == 0:
                    for item in self.items:
                        bl = item[1]
                        if bl.is_conveyor:
                            bl.move_item(item)
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
        elif self.menu == "map":
            wheel = self.input_manager.get_mousewheel()
            if wheel != 0:
                self.map_zoom = max(min(self.map_zoom + wheel / 10, 15), 1)
            #
            move_keys = [#перемещение камеры
                keys[pygame.K_s],
                keys[pygame.K_a],
                keys[pygame.K_w],
                keys[pygame.K_d]
            ]
            if sum(move_keys) > 0:
                if move_keys[1] + move_keys[3] == 0:
                    if move_keys[0]:
                        self.map_pos[1] -= self.map_speed
                    elif move_keys[2]:
                        self.map_pos[1] += self.map_speed
                elif move_keys[0] + move_keys[2] == 0:
                    if move_keys[3]:
                        self.map_pos[0] -= self.map_speed
                    elif move_keys[1]:
                        self.map_pos[0] += self.map_speed
                else:
                    if move_keys[0]:
                        if move_keys[3]:
                            self.map_pos[0] -= self.map_speed / 1.4
                            self.map_pos[1] -= self.map_speed / 1.4
                        elif move_keys[1]:
                            self.map_pos[0] += self.map_speed / 1.4
                            self.map_pos[1] -= self.map_speed / 1.4
                    elif move_keys[2]:
                        if move_keys[3]:
                            self.map_pos[0] -= self.map_speed / 1.4
                            self.map_pos[1] += self.map_speed / 1.4
                        elif move_keys[1]:
                            self.map_pos[0] += self.map_speed / 1.4
                            self.map_pos[1] += self.map_speed / 1.4
            #
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                        self.menu = "game"
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                    dx, dy = event.rel
                    self.map_pos[0] += dx / self.map_zoom
                    self.map_pos[1] += dy / self.map_zoom

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
                if self.test_for_block_pos((x, y)):
                    if self.player.fog[x][y] != 0:
                        if self.action_type == "clear":
                            self.player.task_field[x][y] = 0
                            if self.field[x][y].type == "work in progress":
                                self.field[x][y] = Air(self, (x, y))
                        if self.action_type == "dig":
                            if self.field[x][y].can_mined:
                                self.player.task_field[x][y] = 1
                        if self.action_type == "remove":
                            if self.field[x][y].player == self.player and self.field[x][y].is_construction:
                                self.player.task_field[x][y] = 1
                        if self.action_type == "remove all":
                            self.player.task_field[x][y] = 0
                            if self.field[x][y].type == "work in progress":
                                self.field[x][y] = Air(self, (x, y))
                            if (self.field[x][y].is_construction and self.field[x][y].player == self.player) or self.field[x][y].can_mined:
                                self.player.task_field[x][y] = 1
        #
        if self.action_type != "units":
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
        if self.menu == "game":
            d = 0
            count = [math.ceil(self.display_W / (self.zoom * 256)), math.ceil(self.display_H / (self.zoom * 256))]#количество видимых чанков
            for x in range(int(self.cam_pos[0] / 256 - count[0] / 2), int(self.cam_pos[0] / 256 + count[0] / 2) + 1):
                for y in range(int(self.cam_pos[1] / 256 - count[1] / 2), int(self.cam_pos[1] / 256 + count[1] / 2) + 1):
                    if x >= 0 and x < self.ch_w and y >= 0 and y < self.ch_h:
                        self.chunks[x][y].draw(screen)
                        d += 1
            #
            for item in self.items:
                if item[1].type == "conveyor":
                    pos = item[1].pos
                    img = pygame.transform.scale(items[item[0]], (16 * self.zoom, 16 * self.zoom))
                    screen.blit(img, self.game_to_display([pos[0] * 16, pos[1] * 16]))
                #screen.blit(pygame.transform.scale(dig_img, (16 * self.zoom, 16 * self.zoom)), self.game_to_display([item[1].pos[0] * 16, item[1].pos[1] * 16]))
            #
            blockpos = [
                int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
            ]
            if self.test_for_block_pos(blockpos):
                bl = self.field[blockpos[0]][blockpos[1]]
                if bl.player == self.player:
                    if bl.type == "sorter" or bl.type == "inverted sorter":
                        img = pygame.transform.scale(items[bl.config], (16 * self.zoom, 16 * self.zoom))
                        screen.blit(img, self.game_to_display([bl.pos[0] * 16, bl.pos[1] * 16 - 16]))
                    if bl.type == "drill":
                        if bl.has_ore:
                            img = pygame.transform.scale(items[bl.config], (16 * self.zoom, 16 * self.zoom))
                        else:
                            img = pygame.transform.scale(items[""], (16 * self.zoom, 16 * self.zoom))
                        screen.blit(img, self.game_to_display([bl.pos[0] * 16, bl.pos[1] * 16 - 16]))
                    if bl.is_construction:
                        img = pygame.transform.scale(hbbar[int(10 - bl.health / bl.max_health * 10)], (16 * self.zoom, 16 * self.zoom))
                        screen.blit(img, self.game_to_display([bl.pos[0] * 16, bl.pos[1] * 16 + 16]))
                    if bl.type == "stone turret":
                        img = pygame.transform.scale(progressbar[int(10 - bl.items / bl.max_items * 10)],(16 * self.zoom, 16 * self.zoom))
                        screen.blit(img, self.game_to_display([bl.pos[0] * 16, bl.pos[1] * 16 + 16]))
                if (bl.type == "air" or bl.type == "drill") and self.ore_field[blockpos[0]][blockpos[1]] != None:
                    ore = self.ore_field[blockpos[0]][blockpos[1]]
                    if ore[0] != "coal":
                        img = pygame.transform.scale(selection_img, (16 * self.zoom, 16 * self.zoom))
                        screen.blit(img, self.game_to_display([bl.pos[0] * 16, bl.pos[1] * 16]))
                        render_text(ore[0] + ": " + str(ore[1]), self.game_to_display([bl.pos[0] * 16, bl.pos[1] * 16]), screen, color=(0, 0, 0), centery="down", font=font)
                    else:
                        img = pygame.transform.scale(white_selection_img, (16 * self.zoom, 16 * self.zoom))
                        screen.blit(img, self.game_to_display([bl.pos[0] * 16, bl.pos[1] * 16]))
                        render_text(ore[0] + ": " + str(ore[1]), self.game_to_display([bl.pos[0] * 16, bl.pos[1] * 16]), screen, color=(255, 255, 255), centery="down", font=font)
            #
            for obj in self.objects:
                obj.draw(screen)
            #
            '''for x in range(int(self.cam_pos[0] / 256 - count[0] / 2), int(self.cam_pos[0] / 256 + count[0] / 2) + 1):#туман войны
                for y in range(int(self.cam_pos[1] / 256 - count[1] / 2), int(self.cam_pos[1] / 256 + count[1] / 2) + 1):
                    if x >= 0 and x < self.ch_w and y >= 0 and y < self.ch_h:
                        screen.blit(self.chunks[x][y].scaled_fog_image, self.game_to_display((x * 256, y * 256)))'''
            #
            if self.action_type != None:
                pos = self.game_to_display(self.action_pos)
                mpos = self.display_to_game(mousepos)
                img = pygame.Surface((abs(mousepos[0] - pos[0]), abs(mousepos[1] - pos[1])), pygame.SRCALPHA)
                if self.action_type != "units":
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
                elif self.action_type == "dig" or self.action_type == "remove" or self.action_type == "remove all":
                    img.fill((255, 0, 0, 100))
                elif self.action_type == "clear":
                    img.fill((0, 100, 255, 100))
                #
                if self.action_type == "units":
                    screen.blit(img, (min(pos[0], mousepos[0]),
                                      min(pos[1], mousepos[1])))
                else:
                    corn_pos = self.game_to_display([min(mpos[0], self.action_pos[0]) // 16 * 16, min(mpos[1], self.action_pos[1]) // 16 * 16])
                    screen.blit(img, (min(pos[0], corn_pos[0]),
                                      min(pos[1], corn_pos[1])))
            #
            if self.test_for_block_pos(blockpos) and self.select_block != None and self.field[blockpos[0]][blockpos[1]].type == "air":
                if self.player.fog[blockpos[0]][blockpos[1]] != 0:
                    img = get_block_preview(self.select_block, rotate=self.select_rotate)
                    screen.blit(pygame.transform.scale(img, (16 * self.zoom, 16 * self.zoom)), self.game_to_display((blockpos[0] * 16, blockpos[1] * 16)))
            #
            screen.blit(self.minimap_background, (W - self.w - 18, 0))
            screen.blit(self.minimap, (self.display_W - self.w - 9, 9))
            screen.blit(self.fog_minimap, (self.display_W - self.w - 9, 9))
            pos1 = [min(max((self.cam_pos[0] - W / self.zoom / 2) // 16, 0), self.w - 2), max(min((self.cam_pos[1] - H / self.zoom / 2) // 16, self.h - 2), 0)]#левый верхний
            pos2 = [min(max((self.cam_pos[0] + W / self.zoom / 2) // 16, 0), self.w - 2), max(min((self.cam_pos[1] - H / self.zoom / 2) // 16, self.h - 2), 0)]#правый верхний
            pos3 = [min(max((self.cam_pos[0] - W / self.zoom / 2) // 16, 0), self.w - 2), max(min((self.cam_pos[1] + H / self.zoom / 2) // 16, self.h - 2), 0)]#левый нижний
            pos4 = [min(max((self.cam_pos[0] + W / self.zoom / 2) // 16, 0), self.w - 2), max(min((self.cam_pos[1] + H / self.zoom / 2) // 16, self.h - 2), 0)]#правый нижний
            pygame.draw.rect(screen, (255, 190, 0), (W - self.w - 9 + pos1[0], pos1[1] + 9, pos2[0] - pos1[0], 2))
            pygame.draw.rect(screen, (255, 190, 0), (W - self.w - 9 + pos3[0], pos3[1] + 9, pos4[0] - pos3[0], 2))
            pygame.draw.rect(screen, (255, 190, 0), (W - self.w - 9 + pos1[0], pos1[1] + 9, 2, pos3[1] - pos1[1]))
            pygame.draw.rect(screen, (255, 190, 0), (W - self.w - 9 + pos2[0], pos2[1] + 9, 2, pos4[1] - pos2[1] + 2))
            #
            screen.blit(inventory_background, (W - 268, H - 332))
            #pygame.draw.rect(screen, (90, 90, 90), (W - 320, H - 256, 320, 256))
            screen.blit(inventory_conveyor_img, (W - 64 - 6, H - 320 - 6))
            screen.blit(inventory_drill_img, (W - 64 - 6, H - 256 - 6))
            screen.blit(inventory_factory_img, (W - 64 - 6, H - 192 - 6))
            screen.blit(inventory_turret_img, (W - 64 - 6, H - 128 - 6))
            screen.blit(inventory_unit_img, (W - 64 - 6, H - 64 - 6))
            screen.blit(inventory_selection, (W - 64 - 6, H - 64 * (5 - self.page_index) - 6))
            for i in range(len(pages[self.page_index])):
                bl = pages[self.page_index][i]
                x = W - (4 - (i % 3)) * 64 - 6 + 32 - 24
                y = H - (5 - int(i / 3)) * 64 - 6 + 32 - 24
                screen.blit(get_block_image(bl), (x, y))
                if self.select_block == bl:
                    screen.blit(inventory_selection, (x - 8, y - 8))
            #
            screen.blit(items_background, (W/2 - 360, 0))
            screen.blit(pygame.transform.scale(items["stone"], (48, 48)), (W/2 - 360, 0))
            render_text(":" + str(self.player.resources["stone"]), (W/2 + 40 - 360, 24), screen, color=(255, 255, 255), font=font, centery="center")
            screen.blit(pygame.transform.scale(items["coal"], (48, 48)), (W / 2 - 240, 0))
            render_text(":" + str(self.player.resources["coal"]), (W / 2 + 40 - 240, 24), screen, color=(255, 255, 255), font=font, centery="center")
            screen.blit(pygame.transform.scale(items["iron"], (48, 48)), (W / 2 - 120, 0))
            render_text(":" + str(self.player.resources["iron"]), (W / 2 + 40 - 120, 24), screen, color=(255, 255, 255), font=font, centery="center")
            screen.blit(pygame.transform.scale(items["copper"], (48, 48)), (W / 2, 0))
            render_text(":" + str(self.player.resources["copper"]), (W / 2 + 40, 24), screen, color=(255, 255, 255), font=font, centery="center")
            screen.blit(pygame.transform.scale(items["iron bar"], (48, 48)), (W / 2 + 120, 0))
            render_text(":" + str(self.player.resources["iron bar"]), (W / 2 + 40 + 120, 24), screen, color=(255, 255, 255), font=font, centery="center")
            screen.blit(pygame.transform.scale(items["copper bar"], (48, 48)), (W / 2 + 240, 0))
            render_text(":" + str(self.player.resources["copper bar"]), (W / 2 + 40 + 240, 24), screen, color=(255, 255, 255), font=font, centery="center")
            #
            utils.render_text(str(self.zoom), (0, 25), screen, color=(255, 0, 0))
            utils.render_text(str(d), (0, 50), screen, color=(255, 0, 0))
            utils.render_text(str(self.cam_pos), (0, 75), screen, color=(255, 0, 0))
            utils.render_text("pause: " + str(self.pause), (0, 100), screen, color=(255, 0, 0))
            utils.render_text("draw path: " + str(self.draw_path), (0, 125), screen, color=(255, 0, 0))
            utils.render_text("draw command: " + str(self.draw_command), (0, 150), screen, color=(255, 0, 0))
            utils.render_text("draw path index: " + str(self.draw_path_index), (0, 175), screen, color=(255, 0, 0))
            utils.render_text("draw pos: " + str(self.draw_pos), (0, 200), screen, color=(255, 0, 0))
            utils.render_text("player index: " + str(self.pl_ind), (0, 225), screen, color=(255, 0, 0))
            if self.draw_pos:
                blockpos = [
                    int((self.cam_pos[0] * self.zoom - self.display_W / 2 + mousepos[0]) // (16 * self.zoom)),
                    int((self.cam_pos[1] * self.zoom - self.display_H / 2 + mousepos[1]) // (16 * self.zoom))
                ]
                if self.test_for_block_pos(blockpos):
                    utils.render_text(str(blockpos) + ", " + self.field[blockpos[0]][blockpos[1]].type, mousepos, screen, color=(255, 0, 0))
                else:
                    utils.render_text(str(blockpos), mousepos, screen, color=(255, 0, 0))
        elif self.menu == "map":
            mpos = [
                (self.map_pos[0] - self.w) * self.map_zoom + W / 2,
                (self.map_pos[1] - self.h) * self.map_zoom + H / 2,
            ]
            pygame.draw.rect(screen, (255, 255, 255), (mpos[0] - 2, mpos[1] - 2, self.w * self.map_zoom + 4, self.h * self.map_zoom + 4))
            screen.blit(pygame.transform.scale(self.minimap, (self.w * self.map_zoom, self.h * self.map_zoom)), mpos)
            #
            for obj in self.objects:
                if obj._class == "unit":
                    pos = [
                        (self.map_pos[0] - self.w + obj.pos[0]/16) * self.map_zoom + W / 2,
                        (self.map_pos[1] - self.h + obj.pos[1]/16) * self.map_zoom + H / 2,
                    ]
                    if obj.player == self.player:
                        color = (0, 0, 255)
                    else:
                        color = (255, 0, 0)
                    pygame.draw.rect(screen, color, (pos[0], pos[1], obj.w/16 * self.map_zoom, obj.h/16 *self.map_zoom))
            screen.blit(pygame.transform.scale(self.fog_minimap, (self.w * self.map_zoom, self.h * self.map_zoom)), mpos)
        #
        for button in self.buttons:
            button.draw(screen)

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

    def update_minimap(self, pos):
        if self.field[pos[0]][pos[1]].type == "air":
            if self.ground_field[pos[0]][pos[1]].type == "grass":
                pygame.draw.rect(self.minimap, (0, 167, 0), (pos[0], pos[1], 1, 1))
            elif self.ground_field[pos[0]][pos[1]].type == "sand":
                pygame.draw.rect(self.minimap, (251, 222, 133), (pos[0], pos[1], 1, 1))
            elif self.ground_field[pos[0]][pos[1]].type == "stone floor":
                pygame.draw.rect(self.minimap, (70, 70, 70), (pos[0], pos[1], 1, 1))
        elif self.field[pos[0]][pos[1]].type == "water":
            pygame.draw.rect(self.minimap, (0, 133, 254), (pos[0], pos[1], 1, 1))
        elif self.field[pos[0]][pos[1]].type == "stone":
            pygame.draw.rect(self.minimap, (105, 105, 105), (pos[0], pos[1], 1, 1))
        self.update_fog_minimap(pos)

    def update_fog_minimap(self, pos):
        if self.player.fog[pos[0]][pos[1]] == 0:
            self.fog_minimap.set_at(pos, (0, 0, 0))
        elif self.player.fog[pos[0]][pos[1]] == 1:
            c = self.minimap.get_at(pos)
            self.fog_minimap.set_at(pos, c)
            img = pygame.Surface((1, 1), pygame.SRCALPHA)
            img.fill((0, 0, 0, 128))
            self.fog_minimap.blit(img, pos)
        elif self.player.fog[pos[0]][pos[1]] == 2:
            self.fog_minimap.set_at(pos, (0, 0, 0, 0))