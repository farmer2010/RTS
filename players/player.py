class Player():
    def __init__(self, world):
        self.world = world
        self.selected_units = []#выделенные юниты игрока
        self.resources = {
            "stone" : 0,
            "coal" : 1000,
            "iron" : 1000,
            "iron bar" : 1000,
            "steel" : 1000,
            "copper" : 1000,
            "copper bar" : 1000,
        }
        self.fog = [[0 for y in range(self.world.h)] for x in range(self.world.w)]#0 - туман, 1 - неактивная область, 2 - активная область
        self.task_field = [[0 for y in range(self.world.h)] for x in range(self.world.w)]#0 - нет, 1 - копать, <block> - ставить блок
        self.task_units = [[None for y in range(self.world.h)] for x in range(self.world.w)]
        self.fog_units =  [[[] for y in range(self.world.h)] for x in range(self.world.w)]

    def update(self, events):
        pass

    def command_unit(self, unit, command):#дать команду юниту
        unit.path = unit.pathfind((int(unit.pos[0] // 16), int(unit.pos[1] // 16)), (command[0], command[1]))
        unit.path_index = 0