class FactoryUnit():
    def __init__(self, world, player, block):
        self._class = "factory unit"
        self.world = world
        self.player = player
        self.block = block

    def update(self, events):
        print(self.block.items)
        if self.block.items[self.block.recipe["result"][0]] > 0 and self.block.item == None:
            itm = [self.block.recipe["result"][0], self.block]
            self.block.item = itm
            self.world.items.append(itm)
        #
        if self.block.timer == 0:
            for item in self.block.recipe["cost"]:
                if not self.block.items[item[0]] >= item[1]:
                    return
            if self.block.items[self.block.recipe["result"][0]] >= 20:
                return
            #
            self.block.timer = self.block.production_time
            for item in self.block.recipe["cost"]:
                self.block.items[item[0]] -= item[1]
            itm = [self.block.recipe["result"][0], self.block]
            if self.block.item == None:
                self.block.item = itm
                self.world.items.append(itm)
            else:
                self.block.items[itm[0]] += 1
        else:
            self.block.timer -= 1

    def draw(self, screen):
        pass