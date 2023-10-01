import pygame

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
                             "Each players pays 5 gold to the stranger.",
                             "Take their change and run. (+3 chaos )",
                             "Empty pockets, receive blessings"
                         ],
                         img=pygame.image.load("src/sprites/nce/beggar.png"))

    def update(self):
        super().update()

    def draw(self, screen):
        super().draw(screen)
