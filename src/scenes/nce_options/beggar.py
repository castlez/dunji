import pygame

from src.settings import Settings as settings
from src.classes.traits.giver import Giver
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

    def resolve(self, choice):
        super().resolve(choice)
        match choice:
            case 0:
                settings.chaos = 0
                for player in settings.players:
                    # also technically clears debt
                    settings.log.info(f"{player.name} emptied their pockets.", player)
                    player.inven[0].count = 0
            case 1:
                for player in settings.players:
                    settings.log.info("gave 5 gold to the beggar.", player)
                    player.inven[0].count -= 5
            case 2:
                for player in settings.players:
                    settings.log.info("stole 5 gold from the beggar.", player)
                    player.inven[0].count += 5
                settings.chaos += 3

    def update(self):
        super().update()

    def draw(self, screen):
        super().draw(screen)
