import pygame
from src.settings import Settings as settings


class Mouse:

    @classmethod
    def get_pos(cls):
        """
        :return: the mouse pos scaled by settings.SCALEFACTOR
        """
        return pygame.mouse.get_pos()[0] / settings.SCALEFACTOR, pygame.mouse.get_pos()[1] / settings.SCALEFACTOR

    @classmethod
    def get_pressed(cls):
        return pygame.mouse.get_pressed()