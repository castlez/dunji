import pygame

from src.engine import coords
from src.items.base import Item
from src.settings import Settings as settings


class Shuriken(Item):

    def __init__(self):
        super().__init__(name="Shuriken",
                         description="Deal 5 range dmg",
                         img=pygame.image.load("src/sprites/items/shuriken.png"),
                         value=10)
        self.target = None
        self.rect = self.img.get_rect()

    def use(self, target):
        self.target = target

    def update(self):
        if self.target:
            self.rect.topleft = coords.get_next_pos_towards(self.rect.topleft, self.target.rect.topleft, 10)
            if self.rect.colliderect(self.target.rect):
                settings.log.info("is hit with a shuriken!", self.target)
                self.target.take_damage(5)
                self.target = None

    def draw(self, screen):
        if self.target:
            screen.blit(self.img, self.rect.topleft)