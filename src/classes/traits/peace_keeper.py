import pygame

from src.classes.traits.base import Trait

class PeaceKeeper(Trait):

    def __init__(self):
        super().__init__(name="PeaceKeeper",
                         description="Deescalates conflicts, lowers chaos",
                         img=pygame.image.load("sprites/traits/peaceKeeper.png"))

    def action(self):
        return True