import pygame

from src.settings import Settings as settings
from src.statuses.base import Status


class Confused(Status):

    def __init__(self, target, duration):
        super().__init__(name="Rage",
                         description="Double damage in and out",
                         duration=duration,
                         img=pygame.image.load("src/sprites/statuses/rage.png"),
                         target=target)

    def enact(self):
        if self.duration > 0:
            self.target.bonus_damage = lambda d: d * 2
            self.target.bonus_damage_taken = lambda d: d * 2
            self.duration -= 1
            settings.log.info(f"has rage is active (left: {self.duration})", self.target)
        else:
            settings.log.info("'s rage has ended", self.target)
            self.target.bonus_damage = None
            self.target.bonus_damage_taken = None
