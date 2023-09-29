import pygame

from src.classes.traits.base import Trait


class Hoarder(Trait):

    def __init__(self):
        super().__init__(name="Hoarder",
                         description="Only lets values go when necessary",
                         img=pygame.image.load("sprites/traits/hoarder.png"))

    def action(self):
        return True