import pygame

from src.classes.traits.base import Trait


class NeutralAlignment(Trait):

    def __init__(self):
        super().__init__(name="Neutral",
                         description="Balance in all things",
                         img=pygame.image.load("src/sprites/traits/alignment/neutral.png"))
