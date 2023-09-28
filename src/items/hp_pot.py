import pygame

from src.items.base import Item


class HPPot(Item):

    def __init__(self):
        super().__init__(name="HP Potion",
                         description="Heals 10 HP",
                         img=pygame.image.load("src/sprites/items/hp_pot.png"),
                         value=10)

    def use(self, target):
        target.hp += 10
        if target.hp > target.max_hp:
            target.hp = target.max_hp
