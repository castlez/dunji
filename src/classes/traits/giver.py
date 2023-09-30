import pygame

from src.classes.traits.base import Trait

class Giver(Trait):

    def __init__(self):
        super().__init__(name="Giver",
                         description="Inventory available to party",
                         img=pygame.image.load("src/sprites/traits/giver.png"))

    def action(self):
        return True
