import pygame

from src.engine import coords
from src.items.base import Item


class Shuriken(Item):

    def __init__(self):
        super().__init__(name="Shuriken",
                         description="Deal 5 damage at range",
                         img=pygame.image.load("src/sprites/items/shuriken.png"),
                         value=10)
        self.target = None

    def use(self, target):
        self.target = target

    def update(self):
        if self.target:
            self.rect = coords.get_next_pos_towards(self.rect.topleft, self.target.rect.topleft, 10)
            if self.rect.colliderect(self.target.rect):
                self.target.take_damage(5)
                self.target = None

    def draw(self, screen):
        if self.target:
            screen.blit(self.img, self.rect.topleft)