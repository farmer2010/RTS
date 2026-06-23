from units.unit import *

class Tank(Unit):
    def __init__(self, world, player, pos):
        Unit.__init__(self, world, player, "tank", pos, 30, 30, fog_radius=20, speed=2.5)

    def update(self, events):
        Unit.update(self, events)