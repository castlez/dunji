import pygame.image

from src.classes.traits.base import Trait
from src.items.candy import Candy


class SweetTooth(Trait):

    def __init__(self):
        super().__init__(name="Sweet Tooth",
                         description="Eating candy grants an additional action",
                         img=pygame.image.load("sprites/traits/sweet_tooth.png"))

    def action(self, shops):
        """
        iterates through available shops and
        always picks the one with candy if there is one
        :param shops: list of shops
        :return: shop with candy, else None
        """
        for shop in shops:
            if Candy in [type(i) for i in shop.wares]:
                return shop
        else:
            return None
