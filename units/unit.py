import pygame
from entity import *
import math
from random import randint as rand
from projectiles.projectile import *
import heapq
from textures import *

font = pygame.font.SysFont(None, 24)

class Unit(Entity):
    def __init__(self, world, player, _type, pos, w, h, speed=3, fog_radius=15, health=100, reload=10):
        Entity.__init__(self, world, player, "unit", pos, w, h)
        self.type = _type
        self.speed = speed
        self.health = health
        self.max_health = health
        self.path = []
        self.path_index = 0
        self.reload = reload
        self.target = None
        self.command = None
        self.player.units.append(self)
        self.image.fill((255, 0, 0))
        self.inv_flag = 0#юнит неуязвим?
        self.stop_timer = 0#счетчик шагов, в течение которых юнит не двигался
        self.stop_flag = 0#юнит доехал до конечной точки?
        self.fog_radius = fog_radius
        #
        self.update_unit_field("add")
        self.update_fog("add", [self.pos[0] // 16, self.pos[1] // 16])
        self.fog_presets = self.generate_fog_presets(fog_radius)
        self.reload_timer = 0
        #
        self.can_shoot = 0
        #
        self.movelist4 = [
            [0, -1],
            [1, 0],
            [0, 1],
            [-1, 0]
        ]

    def update(self, events):
        #
        #СТРЕЛЬБА
        #
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
            self.world.objects.append(Projectile(self.world, self.player, self.pos.copy(), 5, 5, rotate, 5, self.fog_radius*16, 10))
            self.reload_timer = self.reload
        if self.reload_timer > 0:
            self.reload_timer -= 1
        #
        #
        #
        self.move_path()
        #
        keys = pygame.key.get_pressed()
        move_keys = [
            keys[pygame.K_UP],
            keys[pygame.K_RIGHT],
            keys[pygame.K_DOWN],
            keys[pygame.K_LEFT]
        ]
        if sum(move_keys) > 0 and self in self.player.selected_units:
            self.path = []
            self.command = None
            if move_keys[1] + move_keys[3] == 0:
                if move_keys[0]:
                    self.move(self.speed, 1.5 * math.pi)
                elif move_keys[2]:
                    self.move(self.speed, 0.5 * math.pi)
            elif move_keys[0] + move_keys[2] == 0:
                if move_keys[3]:
                    self.move(self.speed, math.pi)
                elif move_keys[1]:
                    self.move(self.speed, 0)
            else:
                if move_keys[0]:
                    if move_keys[3]:
                        self.move(self.speed, 1.25 * math.pi)
                    elif move_keys[1]:
                        self.move(self.speed, 1.75 * math.pi)
                elif move_keys[2]:
                    if move_keys[3]:
                        self.move(self.speed, 0.75 * math.pi)
                    elif move_keys[1]:
                        self.move(self.speed, 0.25 * math.pi)
        #
        #РАСТАЛКИВАНИЕ
        #
        collide = self.collide(0, 0)
        coll_obj = collide[3]
        if collide[0]:
            if coll_obj != None and coll_obj._class == "unit":
                if not coll_obj.inv_flag and not self.inv_flag:
                    sp = 3
                    rotate = math.atan2(coll_obj.pos[1] - self.pos[1], coll_obj.pos[0] - self.pos[0])
                    rotate = rotate - math.pi
                    dx = math.cos(rotate) * sp
                    dy = math.sin(rotate) * sp
                    self.pos[0] += dx
                    collide_x = self.collide((dx < 0) * 2 - 1, 0)
                    un_x = 0
                    if collide_x[3] != None and collide_x[3]._class == "unit":
                        un_x = 1
                    if collide_x[0] and not un_x:
                        if dx > 0.01:
                            self.pos[0] = collide_x[1] - self.w / 2
                        elif dx < 0.01:
                            self.pos[0] = collide_x[1] + self.w / 2
                    #
                    self.pos[1] += dy
                    collide_y = self.collide(0, (dy < 0) * 2 - 1)
                    un_y = 0
                    if collide_y[3] != None and collide_y[3]._class == "unit":
                        un_y = 1
                    if collide_y[0] and not un_y:
                        if dy > 0.01:
                            self.pos[1] = collide_y[2] - self.h / 2
                        elif dy < 0.01:
                            self.pos[1] = collide_y[2] + self.h / 2

    def move_command(self, pos, move_to_close=0):
        if self.world.test_for_block_pos(pos):
            self.path = self.pathfind((int((self.pos[0] - self.w / 2) // 16), int((self.pos[1] - self.h / 2) // 16)),(pos[0], pos[1]), move_to_close=move_to_close)
            self.path_index = 1
            if len(self.path) > 0:
                self.command = ((pos[0], pos[1]), self.world.command_index)
            else:
                self.command = None
        self.stop_flag = 0

    def generate_fog_presets(self, fog_radius):
        """
        Генерирует пресеты изменения тумана войны для 8 направлений движения

        Args:
            fog_radius: радиус обзора юнита

        Returns:
            Словарь, где ключ - направление (0-7), значение - кортеж (удаляемые_клетки, добавляемые_клетки)
            Направления: 0-вверх, 1-вверх-вправо, 2-вправо, 3-вниз-вправо,
                         4-вниз, 5-вниз-влево, 6-влево, 7-влево-вверх
        """

        # Рассчитываем все клетки в радиусе обзора
        radius_int = fog_radius

        # Векторы движения для 8 направлений
        direction_vectors = [
            (0, -1),  # вверх
            (1, -1),  # вверх-вправо
            (1, 0),  # вправо
            (1, 1),  # вниз-вправо
            (0, 1),  # вниз
            (-1, 1),  # вниз-влево
            (-1, 0),  # влево
            (-1, -1)  # влево-вверх
        ]

        presets = []

        for direction in range(8):
            dx, dy = direction_vectors[direction]

            # Множества клеток для старой и новой позиции
            # Смещаем все клетки на вектор движения
            new_cells = []
            old_cells = []

            # Для каждой клетки в радиусе определяем, изменится ли ее состояние
            for cx in range(-radius_int - 1, radius_int + 2):
                for cy in range(-radius_int - 1, radius_int + 2):
                    # Новая позиция клетки после движения юнита
                    new_cx, new_cy = cx + dx, cy + dy

                    # Проверяем, была ли эта клетка видна раньше и видна ли сейчас
                    was_visible = cx ** 2 + cy ** 2 <= fog_radius ** 2
                    will_be_visible = new_cx ** 2 + new_cy ** 2 <= fog_radius ** 2

                    # Если клетка была видна, но перестанет быть видимой - удаляем
                    if was_visible and not will_be_visible:
                        old_cells.append((cx, cy))

                    # Если клетка не была видна, но станет видимой - добавляем
                    #print((cx, cy), was_visible, will_be_visible)
                    if not was_visible and will_be_visible:
                        new_cells.append((new_cx, new_cy))
            presets.append([old_cells, new_cells])
        return presets

    def update_fog(self, func, pos):
        if self.player == self.world.player:
            for x in range(int(pos[0] - self.fog_radius), int(pos[0] + self.fog_radius + 1)):
                for y in range(int(pos[1] - self.fog_radius), int(pos[1] + self.fog_radius + 1)):
                    if self.world.test_for_block_pos((x, y)) and (pos[0] - x) ** 2 + (pos[1] - y) ** 2 <= self.fog_radius ** 2:
                        if func == "remove":
                            if self in self.player.fog_units[x][y]:
                                self.player.fog_units[x][y].remove(self)
                            if len(self.player.fog_units[x][y]) == 0:
                                self.player.fog[x][y] = 1
                                self.world.chunks[int(x // 16)][int(y // 16)].fog_blocks[x % 16][y % 16].blit(self.world.ground_field[x][y].get_image())
                                self.world.chunks[int(x // 16)][int(y // 16)].fog_blocks[x % 16][y % 16].blit(self.world.field[x][y].get_image())
                        elif func == "add":
                            if self not in self.player.fog_units[x][y]:
                                self.player.fog_units[x][y].append(self)
                            if self in self.player.fog_units[x][y]:
                                self.player.fog[x][y] = 2
            #
            count = [math.ceil(self.fog_radius * 2 / 16), math.ceil(self.fog_radius * 2 / 16)]  # количество видимых чанков
            for x in range(int(self.pos[0] / 256 - count[0] / 2), int(self.pos[0] / 256 + count[0] / 2) + 1):
                for y in range(int(self.pos[1] / 256 - count[1] / 2), int(self.pos[1] / 256 + count[1] / 2) + 1):
                    if x >= 0 and x < self.world.ch_w and y >= 0 and y < self.world.ch_h:
                        self.world.chunks[x][y].fog_changes = 1

    def update_unit_field(self, func):
        for x in range(int((self.pos[0] - self.w/2) // 16), int((self.pos[0] + self.w/2) // 16) + 1):
            for y in range(int((self.pos[1] - self.h/2) // 16), int((self.pos[1] + self.h/2) // 16) + 1):
                if self.world.test_for_block_pos((x, y)):
                    if func == "remove":
                        if self in self.world.unit_field[x][y]:
                            self.world.unit_field[x][y].remove(self)
                    elif func == "add":
                        if self not in self.world.unit_field[x][y]:
                            self.world.unit_field[x][y].append(self)

    def kill(self):
        Entity.kill(self)
        #
        self.update_unit_field("remove")
        self.update_fog("remove", [self.pos[0] // 16, self.pos[1] // 16])
        #
        if self in self.player.selected_units:
            self.player.selected_units.remove(self)
        self.player.units.remove(self)

    def move(self, speed, rotate):
        moves = {
            (0, -1): 0,
            (1, -1): 1,
            (1, 0): 2,
            (1, 1): 3,
            (0, 1): 4,
            (-1, 1): 5,
            (-1, 0): 6,
            (-1, -1): 7
        }
        #
        self.update_unit_field("remove")
        pos = [int(self.pos[0] // 16), int(self.pos[1] // 16)]
        c = 1
        if self.world.test_for_block_pos(pos):
            c = self.world.ground_field[pos[0]][pos[1]].speed
        mov = Entity.move(self, speed * c, rotate)
        new_pos = [int(self.pos[0] // 16), int(self.pos[1] // 16)]
        if self.player == self.world.player:
            if new_pos != pos:
                rotate = moves[(new_pos[0] - pos[0], new_pos[1] - pos[1])]
                for p in self.fog_presets[rotate][1]:
                    npos = [pos[0] + p[0], pos[1] + p[1]]
                    if self.world.test_for_block_pos(npos):
                        if self in self.player.fog_units[npos[0]][npos[1]]:
                            self.player.fog_units[npos[0]][npos[1]].remove(self)
                            if len(self.player.fog_units[npos[0]][npos[1]]) == 0:
                                self.player.fog[npos[0]][npos[1]] = 1
                                self.world.chunks[int(npos[0] // 16)][int(npos[1] // 16)].fog_blocks[npos[0] % 16][npos[1] % 16].blit(self.world.ground_field[npos[0]][npos[1]].get_image())
                                self.world.chunks[int(npos[0] // 16)][int(npos[1] // 16)].fog_blocks[npos[0] % 16][npos[1] % 16].blit(self.world.field[npos[0]][npos[1]].get_image())
                #
                for p in self.fog_presets[rotate][0]:
                    npos = [new_pos[0] + p[0], new_pos[1] + p[1]]
                    if self.world.test_for_block_pos(npos):
                        if self not in self.player.fog_units[npos[0]][npos[1]]:
                            self.player.fog_units[npos[0]][npos[1]].append(self)
                            self.player.fog[npos[0]][npos[1]] = 2
                #
                for x in range(int(self.pos[0] / 256 - (self.fog_radius + 1) / 16), int(self.pos[0] / 256 + (self.fog_radius + 1) / 16) + 1):
                    for y in range(int(self.pos[1] / 256 - (self.fog_radius + 1) / 16), int(self.pos[1] / 256 + (self.fog_radius + 1) / 16) + 1):
                        if x >= 0 and x < self.world.ch_w and y >= 0 and y < self.world.ch_h:
                            self.world.chunks[x][y].fog_changes = 1
        self.update_unit_field("add")
        return(mov)

    def move_path(self):
        if self.path_index < len(self.path):
            if self.path_index >= 0:
                rotate = math.atan2(self.path[self.path_index][1] * 16 + self.h/2 + 1 - self.pos[1], self.path[self.path_index][0] * 16 + self.w/2 + 1 - self.pos[0])
                #
                if self.pos[0] > self.path[self.path_index][0] * 16 + self.w/2 + 1 - self.speed and \
                        self.pos[0] < self.path[self.path_index][0] * 16 + self.w/2 + 1 + self.speed and \
                        self.pos[1] > self.path[self.path_index][1] * 16 + self.h/2 + 1 - self.speed and \
                        self.pos[1] < self.path[self.path_index][1] * 16 + self.h/2 + 1 + self.speed:
                    self.path_index += 1
                collide = self.move(self.speed, rotate)
                if collide[0]:
                    self.stop_timer += 1
                else:
                    self.stop_timer = 0
                    self.inv_flag = 0
                if self.stop_timer == 10:
                    self.inv_flag = 1
                if self.stop_timer > 30 and (self.pos[0] // 16 - self.command[0][0]) ** 2 + (self.pos[1] // 16 - self.command[0][1]) ** 2 < 16:
                    self.path = []
                    self.command = None
                    self.inv_flag = 0
                    self.stop_flag = 1
                #if collide:
                #    self.path = self.pathfind((int((self.pos[0] - self.w/2) // 16), int((self.pos[1] - self.h/2) // 16)), (self.command[0][0], self.command[0][1]))
                #    self.path_index = 1
                #elif len(self.path) == 0:
                #    self.path = self.pathfind((int((self.pos[0] - self.w / 2) // 16), int((self.pos[1] - self.h / 2) // 16)), (self.command[0][0], self.command[0][1]))
                #    self.path_index = 1
            else:
                self.path_index += 1
        else:#конец маршрута
            self.path = []
            self.command = None
            self.inv_flag = 0
            self.stop_flag = 1

    def pathfind(self, start_pos, end_pos, move_to_close=0):
        field = self.world.field
        width = len(field)
        height = len(field[0])
        # Проверка корректности начальной и конечной позиций
        if field[start_pos[0]][start_pos[1]].has_hitbox:
            return []
        if not move_to_close:
            if field[end_pos[0]][end_pos[1]].has_hitbox:
                return []
        # Если старт и финиш совпадают
        if start_pos == end_pos:
            return []
        # Стоимость перемещения по диагонали
        DIAGONAL_COST = 1.41
        STRAIGHT_COST = 1.0
        # Список возможных перемещений (8 направлений)
        movelist = [
            [0, -1],  # вверх
            [1, -1],  # вверх-вправо
            [1, 0],  # вправо
            [1, 1],  # вниз-вправо
            [0, 1],  # вниз
            [-1, 1],  # вниз-влево
            [-1, 0],  # влево
            [-1, -1]  # вверх-влево
        ]
        # Словари для хранения данных
        g_score = {start_pos: 0}
        f_score = {start_pos: self.heuristic(start_pos, end_pos)}
        # Словарь для восстановления пути
        came_from = {}
        # Очередь с приоритетом (мин-куча)
        open_set = [(f_score[start_pos], start_pos)]
        open_set_hash = {start_pos}
        # Закрытое множество (посещённые вершины)
        closed_set = set()
        while open_set:
            # Извлекаем вершину с минимальным f_score
            current_f, current = heapq.heappop(open_set)
            open_set_hash.remove(current)
            # Если достигли цели
            if current == end_pos:
                # Восстанавливаем путь
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start_pos)
                path.reverse()
                return path
            closed_set.add(current)
            # Проверяем всех соседей
            for dx, dy in movelist:
                neighbor = (current[0] + dx, current[1] + dy)
                # Проверка выхода за границы карты
                if not (0 <= neighbor[0] < width and 0 <= neighbor[1] < height):
                    continue
                #для рабочих есть возможность подъехать к закрытой клетке
                if move_to_close and neighbor[0] == end_pos[0] and neighbor[1] == end_pos[1] and field[neighbor[0]][neighbor[1]].has_hitbox:
                    # Восстанавливаем путь
                    path = []
                    while current in came_from:
                        path.append(current)
                        current = came_from[current]
                    path.append(start_pos)
                    path.reverse()
                    return path
                # Если сосед уже в закрытом множестве, пропускаем
                if neighbor in closed_set:
                    continue
                # Проверка возможности передвижения
                if not self.test_hitbox(neighbor, self.w, self.h):  # fffff
                    continue
                if dx != 0 and dy != 0:
                    if not self.can_move_diagonal(field, current, neighbor):
                        continue
                # Вычисляем стоимость перехода к соседу
                if dx != 0 and dy != 0:
                    move_cost = DIAGONAL_COST / self.world.ground_field[neighbor[0]][neighbor[1]].speed
                else:
                    move_cost = STRAIGHT_COST / self.world.ground_field[neighbor[0]][neighbor[1]].speed
                tentative_g = g_score[current] + move_cost
                # Если сосед не в открытом множестве или найден лучший путь
                if neighbor not in open_set_hash or tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, end_pos)
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
        # Путь не найден
        return []

    def heuristic(self, a, b):#Эвристическая функция (расстояние Чебышева с учётом диагоналей)
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return 1.41 * min(dx, dy) + abs(dx - dy)

    def test_hitbox(self, pos, w, h):  # может ли юнит проехать на клетку
        count = [math.ceil(w / 16), math.ceil(h / 16)]
        for x in range(pos[0], pos[0] + count[0]):
            for y in range(pos[1], pos[1] + count[1]):
                if x >= 0 and x < len(self.world.field) and y >= 0 and y < len(self.world.field[0]):
                    #if self.world.field[x][y].has_hitbox or (len(self.world.unit_field[x][y]) > 0 and self not in self.world.unit_field[x][y]):
                    if self.world.field[x][y].has_hitbox:
                        return(0)
                else:
                    return(0)
        return(1)

    def can_move_diagonal(self, field, from_pos, to_pos):  # Функция проверки возможности диагонального перемещения
        """
        Проверяет, можно ли переместиться по диагонали.
        Диагональ разрешена, если хотя бы одна из двух прямых клеток
        (горизонтальная или вертикальная) проходима.
        """
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]
        # Проверяем, что это действительно диагональ
        if dx == 0 or dy == 0:
            return True
        # Соседние прямые клетки
        horizontal_neighbor = (from_pos[0] + dx, from_pos[1])  # движение по горизонтали
        vertical_neighbor = (from_pos[0], from_pos[1] + dy)  # движение по вертикали
        # Проверяем, что обе клетки в пределах карты
        h_x, h_y = horizontal_neighbor
        v_x, v_y = vertical_neighbor
        if not (0 <= h_x < len(field) and 0 <= h_y < len(field[0])):
            return False
        if not (0 <= v_x < len(field) and 0 <= v_y < len(field[0])):
            return False
        # Диагональ разрешена, если хотя бы одна из прямых клеток свободна
        return self.test_hitbox((h_x, h_y), self.w, self.h) and self.test_hitbox((v_x, v_y), self.w, self.h)  #можно заменить or на and

    def draw(self, screen):
        pos = [
            round((self.pos[0] - self.world.cam_pos[0] - self.w / 2) * self.world.zoom + self.world.display_W / 2),
            round((self.pos[1] - self.world.cam_pos[1] - self.h / 2) * self.world.zoom + self.world.display_H / 2)
        ]
        screen.blit(pygame.transform.scale(self.image, (self.w * self.world.zoom, self.h * self.world.zoom)), pos)
        if self in self.player.selected_units:
            pygame.draw.circle(screen, (255, 255, 0), [pos[0] + self.w/2*self.world.zoom, pos[1] + self.h/2*self.world.zoom], 10 * self.world.zoom * (self.w / 30))
        #
        if self.world.draw_path:
            for pos in self.path:
                img = pygame.Surface((16 * self.world.zoom, 16 * self.world.zoom), pygame.SRCALPHA)
                img.fill((0, 128, 255, 128))
                screen.blit(img, self.world.game_to_display((pos[0] * 16, pos[1] * 16)))
        p = self.world.game_to_display(self.pos)
        #col = self.collide(0, 0)
        if self.world.draw_path_index:
            screen.blit(font.render(str(self.path_index), 1, (0, 0, 0)), p)
        if self.world.draw_command:
            screen.blit(font.render(str(self.command), 1, (0, 0, 0)), [p[0], p[1] + 15])
        #screen.blit(font.render(str(col[0]) + " " + str(col[3]), 1, (0, 0, 0)), (p[0], p[1] + 15))
        #
        if self.health < self.max_health:
            img = pygame.transform.scale(hbbar[int(10 - self.health / self.max_health * 10)], (16 * self.world.zoom * math.ceil(self.w / 16), 16 * self.world.zoom * math.ceil(self.w / 16)))
            screen.blit(img, self.world.game_to_display([self.pos[0] - 16 * math.ceil(self.w / 16) / 2, self.pos[1] + self.h/2]))