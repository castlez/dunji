import pygame

from src.statuses.base import Status


class Confused(Status):

    def __init__(self, target, duration):
        super().__init__(name="Confused",
                         description="Might attack friends",
                         duration=duration,
                         img=pygame.image.load("src/sprites/statuses/confused.png"),
                         target=target)

    def enact(self):
        if self.duration > 0:
            self.duration -= 1
