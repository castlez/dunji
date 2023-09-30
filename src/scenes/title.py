import pygame

from src.scenes.base import Scene
from src.scenes.party_select import PartySelectScene
from src.settings import Settings as settings


class TitleScene(Scene):
    info_box_pos = None
    info_box = None

    @staticmethod
    def get_map_icon():
        raise NotImplementedError()

    def __init__(self):
        self.img = pygame.image.load("src/sprites/ui/title_screen.png")

    def update(self):
        # if the player clicks, move to map scene
        if pygame.mouse.get_pressed()[0]:
            # TODO go to character select
            settings.current_scene = PartySelectScene()

    def draw(self, screen):
        screen.blit(self.img, (0, 0))
