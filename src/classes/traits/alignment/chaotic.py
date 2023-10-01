import pygame

from src.classes.traits.base import Trait


class ChaoticAlignment(Trait):

    def __init__(self):
        super().__init__(name="Chaotic",
                         description="Does what they want",
                         img=pygame.image.load("src/sprites/traits/alignment/chaotic.png"))
