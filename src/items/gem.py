import pygame

from src.items.base import Item


class Gem(Item):

    def __init__(self):
        super().__init__(name="Gem",
                         description="Probably worth some gold",
                         img=pygame.image.load("src/sprites/items/gem.png"),
                         value=10)

    def use(self, target):
        pass  # this is just sold for gold
