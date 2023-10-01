import pygame

from src.classes.traits.base import Trait


class LawfulAlignment(Trait):

    def __init__(self):
        super().__init__(name="Lawful",
                         description="Follows the rules",
                         img=pygame.image.load("src/sprites/traits/alignment/lawful.png"))