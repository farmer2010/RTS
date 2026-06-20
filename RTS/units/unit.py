import pygame
from entity import *
import math
from random import randint as rand
from projectiles.projectile import *
import heapq

font = pygame.font.SysFont(None, 40)

class Unit(Entity):
    def __init__(self, world, player, pos, w, h):
        Entity.__init__(self, world, player, "unit", pos, w, h)
        self.speed = 3
        self.path = []
        self.path_index = 0
        self.target = None
        self.image.fill((255, 0, 0))

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    mousepos = pygame.mouse.get_pos()
                    pos = [
                        (self.world.cam_pos[0] * self.world.zoom - self.world.display_W / 2 + mousepos[0]) / self.world.zoom,
                        (self.world.cam_pos[1] * self.world.zoom - self.world.display_H / 2 + mousepos[1]) / self.world.zoom
                    ]
                    self.path = self.pathfind((int(self.pos[0] // 16), int(self.pos[1] // 16)), (int(pos[0] // 16), int(pos[1] // 16)))
                    self.path_index = 0
        self.move_path()
        keys = pygame.key.get_pressed()
        move_keys = [
            keys[pygame.K_UP],
            keys[pygame.K_RIGHT],
            keys[pygame.K_DOWN],
            keys[pygame.K_LEFT]
        ]
        if sum(move_keys) > 0:
            self.path = []
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
        #if rand(0, 1) == 0:
        #    mousepos = pygame.mouse.get_pos()
        #    pos = [
        #        (self.world.cam_pos[0] * self.world.zoom - self.world.display_W / 2 + mousepos[0]) / self.world.zoom,
        #        (self.world.cam_pos[1] * self.world.zoom - self.world.display_H / 2 + mousepos[1]) / self.world.zoom
        #    ]
        #    self.world.objects.append(Projectile(self.world, self.pos.copy(), 10, 10, math.atan2(pos[1] - self.pos[1], pos[0] - self.pos[0]), 5, 240))

    def move_path(self):
        moves = {
            (1, 0) : 0,
            (1, 1) : 0.25 * math.pi,
            (0, 1) : 0.5 * math.pi,
            (-1, 1) : 0.75 * math.pi,
            (-1, 0) : math.pi,
            (-1, -1) : 1.25 * math.pi,
            (0, -1) : 1.5 * math.pi,
            (1, -1): 1.75 * math.pi,
        }
        if self.path_index < len(self.path):
            if self.path_index < len(self.path):
                if self.path_index > 0:
                    dx = int(self.path[self.path_index][0] - self.path[self.path_index - 1][0])
                    dy = int(self.path[self.path_index][1] - self.path[self.path_index - 1][1])
                    rotate = moves[(dx, dy)]
                    #
                    if self.pos[0] > self.path[self.path_index][0] * 16 + 8 - self.speed / 2 and \
                            self.pos[0] < self.path[self.path_index][0] * 16 + 8 + self.speed / 2 and \
                            self.pos[1] > self.path[self.path_index][1] * 16 + 8 - self.speed / 2 and \
                            self.pos[1] < self.path[self.path_index][1] * 16 + 8 + self.speed / 2:
                        self.pos = [self.path[self.path_index][0] * 16 + 8, self.path[self.path_index][1] * 16 + 8]
                        self.path_index += 1
                    else:
                        self.move(self.speed, rotate)
                else:
                    if self.pos[0] > self.path[self.path_index][0] * 16 + 8 - self.speed / 2 and \
                            self.pos[0] < self.path[self.path_index][0] * 16 + 8 + self.speed / 2 and \
                            self.pos[1] > self.path[self.path_index][1] * 16 + 8 - self.speed / 2 and \
                            self.pos[1] < self.path[self.path_index][1] * 16 + 8 + self.speed / 2:
                        self.pos = [self.path[self.path_index][0] * 16 + 8, self.path[self.path_index][1] * 16 + 8]
                        self.path_index += 1
                    else:
                        rotate = math.atan2(self.path[self.path_index][1] * 16 + 8 - self.pos[1], self.path[self.path_index][0] * 16 + 8 - self.pos[0])
                        self.move(self.speed, rotate)

    def pathfind(self, start_pos, end_pos):
        field = self.world.field
        width = len(field)
        height = len(field[0])
        # Проверка корректности начальной и конечной позиций
        if field[start_pos[0]][start_pos[1]].has_hitbox:
            return []
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
                # Проверка на стену
                if field[neighbor[0]][neighbor[1]].has_hitbox:
                    continue
                # Если сосед уже в закрытом множестве, пропускаем
                if neighbor in closed_set:
                    continue
                # Проверка возможности диагонального перемещения
                # Если движение диагональное, проверяем условие проходимости
                if not self.test_hitbox(field, neighbor, self.w, self.h):  # fffff
                    continue
                if dx != 0 and dy != 0:
                    if not self.can_move_diagonal(field, current, neighbor):
                        continue
                # Вычисляем стоимость перехода к соседу
                if dx != 0 and dy != 0:
                    move_cost = DIAGONAL_COST
                else:
                    move_cost = STRAIGHT_COST
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

    def test_hitbox(self, field, pos, w, h):  # может ли юнит проехать на клетку
        for x in range(int(pos[0] - round(w / 2 / 16)), int(pos[0] + round(w / 2 / 16) + 1)):
            for y in range(int(pos[1] - round(h / 2 / 16)), int(pos[1] + round(h / 2 / 16) + 1)):
                if x >= 0 and x < len(field) and y >= 0 and y < len(field[0]):
                    if field[x][y].has_hitbox:
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
        return (field[h_x][h_y].has_hitbox == 0) and (field[v_x][v_y].has_hitbox == 0)  # можно заменить or на and
