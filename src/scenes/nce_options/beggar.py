import pygame

from src.settings import Settings as settings
from src.classes.traits.giver import Giver
from src.engine import render
from src.scenes.nce_options.base import NCEOption


class BeggarEvent(NCEOption):

    def __init__(self):
        super().__init__(name="Beggar",
                         prompt=[
                             "A person down on their luck leans against a wall.",
                             "\"Please, friends, I'm hungry. Spare some change?\""
                         ],
                         choices=[
                             "1. [Lawful] Empty pockets, receive blessings (chaos=0).",
                             "2. [Neutral] Each players pays 5 gold to the stranger.",
                             "3. [Chaotic] Take their change and run (+3 chaos).",
                         ],
                         img=pygame.image.load("src/sprites/nce/beggar.png"))

    def check_resolve(self, player):
        if player.check_traits(Giver):
            player.inven[0].count = 0
            self.done = True
            self.outcome = "A giver emptied their pockets (chaos - 3)."
            settings.chaos -= 3
            if settings.chaos < 0:
                settings.chaos = 0
            return

    def update(self):
        super().update()

    def draw(self, screen):
        super().draw(screen)
