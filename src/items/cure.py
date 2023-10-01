import pygame

from src.items.base import Item


class Cure(Item):

    def __init__(self):
        super().__init__(name="Cure Potion",
                         description="Cures all statuses",
                         img=pygame.image.load("src/sprites/items/cure.png"),
                         value=10)

    def use(self, target):
        for status in target.statuses:
            status.duration = 0
