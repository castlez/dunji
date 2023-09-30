import pygame.image

from src.classes.traits.base import Trait


class Clepto(Trait):

    def __init__(self):
        super().__init__(name="Clepto",
                         description="Steals things, causes trouble",
                         img=pygame.image.load("src/sprites/traits/clepto.png"))
