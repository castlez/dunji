import pygame

from src.classes.traits.base import Trait

class Sneaky(Trait):

    def __init__(self):
        super().__init__(name="Sneaky",
                         description="Gets seen last, quite lonely",
                         img=pygame.image.load("src/spritess/traits/sneaky.png"))

    def action(self):
        return True