import pygame

from src.items.base import Item


class Coins(Item):

    def __init__(self):
        super().__init__(name="Gold Coins",
                         description="Buy stuff with it",
                         img=pygame.image.load("src/sprites/items/coin.png"),
                         value=10)
        self.count = 30

    def use(self, target):
        # TODO more random starting money
        # TODO able to get from drops maybe?
        pass
