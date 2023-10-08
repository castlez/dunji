import pygame

from src.settings import Settings as settings
from src.statuses.base import Status


class Confused(Status):

    def __init__(self, target, duration):
        super().__init__(name="Confused",
                         description="Might attack friends or self",
                         duration=duration,
                         img=pygame.image.load("src/sprites/statuses/confused.png"),
                         target=target)

    def enact(self):
        if self.duration > 0:
            self.duration -= 1
            settings.log.info(f"is confused (left: {self.duration})", self.target)
        else:
            settings.log.info("'s confusion ended'", self.target)