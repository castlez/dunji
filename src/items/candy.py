import pygame

from src.items.base import Item


class Candy(Item):

    def __init__(self):
        super().__init__(name="Candy",
                         description="Grants an additional action",
                         img=pygame.image.load("src/sprites/items/candy.png"),
                         value=10)

    def use(self, target):
        target.actions += 1
