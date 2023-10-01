import pygame

from src.classes.traits.base import Trait


class DemonAlignment(Trait):

    def __init__(self):
        super().__init__(name="Demon",
                         description="Truly Evil",
                         img=pygame.image.load("src/sprites/traits/alignment/demon.png"))
