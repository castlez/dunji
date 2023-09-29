import pygame.image

from src.classes.traits.base import Trait
from src.items.candy import Candy


class Clepto(Trait):

    def __init__(self):
        super().__init__(name="Clepto",
                         description="Steals things, causes trouble",
                         img=pygame.image.load("sprites/traits/clepto.png"))

    def action(self):
        return True
