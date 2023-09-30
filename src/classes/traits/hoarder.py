import pygame

from src.classes.traits.base import Trait


class Hoarder(Trait):

    def __init__(self):
        super().__init__(name="Hoarder",
                         description="Hoards all gems",
                         img=pygame.image.load("src/sprites/traits/hoarder.png"))
