import pygame.image

from src.classes.traits.base import Trait
from src.items.candy import Candy


class Hypochondriac(Trait):

    def __init__(self):
        super().__init__(name="Hypochondriac",
                         description="Chugs healing potions",
                         img=pygame.image.load("src/sprites/traits/hypochondriac.png"))
