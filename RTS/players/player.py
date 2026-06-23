class Player():
    def __init__(self, world):
        self.world = world
        self.units = []#все юниты игрока
        self.selected_units = []#выделенные юниты игрока
        self.resources = {
            "stone" : 0,
            "coal" : 0,
            "iron_ore" : 0,
            "iron" : 0,
            "steel" : 0,
            "copper_ore" : 0,
            "copper" : 0,
        }
        self.fog = [[0 for y in range(self.world.h)] for x in range(self.world.w)]#0 - туман, 1 - неактивная область, 2 - активная область
        self.task_field = [[None for y in range(self.world.h)] for x in range(self.world.w)]#0 - нет, 1 - копать, <block> - ставить блок
        self.fog_units =  [[[] for y in range(self.world.h)] for x in range(self.world.w)]

    def update(self, events):
        pass

    def command_unit(self, unit, command):#дать команду юниту
        unit.path = unit.pathfind((int(unit.pos[0] // 16), int(unit.pos[1] // 16)), (command[0], command[1]))
        unit.path_index = 0