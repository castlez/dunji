import pygame

from src.statuses.base import Status


class Poison(Status):

    def __init__(self, target, duration):
        super().__init__(name="Poison",
                         description="Take damage each turn",
                         duration=duration,
                         img=pygame.image.load("src/sprites/statuses/poisoned.png"),
                         target=target)

    def enact(self):
        if self.duration > 0:
            self.target.hp -= 1
            self.duration -= 1
