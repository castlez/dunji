import pygame

from src.classes.traits.base import Trait


class SaintAlignment(Trait):

    def __init__(self):
        super().__init__(name="Saint",
                         description="Truly Good",
                         img=pygame.image.load("src/sprites/traits/alignment/saint.png"))