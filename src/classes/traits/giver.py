import pygame

from src.classes.traits.base import Trait

class Giver(Trait):

    def __init__(self):
        super().__init__(name="Giver",
                         description="Inventory available to party",
                         img=pygame.image.load("sprites/traits/sweet_tooth.png"))

    def action(self):
        return True
