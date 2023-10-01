import pygame

from src.settings import Settings as settings
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
            self.duration -= 1
            settings.log.info(f"is poisoned (left: {self.duration})", self.target)
            self.target.take_damage(1)
        else:
            settings.log.info("'s poison ended'", self.target)
