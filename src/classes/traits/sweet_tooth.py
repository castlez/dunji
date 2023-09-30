import pygame.image

from src.classes.traits.base import Trait
from src.items.candy import Candy


class SweetTooth(Trait):

    def __init__(self):
        super().__init__(name="Sweet Tooth",
                         description="Eating candy grants an additional action",
                         img=pygame.image.load("sprites/traits/sweet_tooth.png"))
