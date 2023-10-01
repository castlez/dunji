import pygame

from src.settings import Settings as settings
from src.statuses.base import Status


class Slow(Status):

    def __init__(self, target, duration):
        super().__init__(name="Slowed",
                         description="Halves movement speed",
                         duration=duration,
                         img=pygame.image.load("src/sprites/statuses/slow.png"),
                         target=target)

    def enact(self):
        if self.duration > 0:
            self.duration -= 1
            settings.log.info(f"is slowed (left: {self.duration})", self.target)
            self.target.speed = self.target.speed // 2
        else:
            self.target.speed = self.target.max_speed
            settings.log.info("'s slow ended'", self.target)