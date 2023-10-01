import pygame
from src.settings import Settings as settings


def get_pos():
    """
    :return: the mouse pos scaled by settings.SCALEFACTOR
    """
    return pygame.mouse.get_pos()[0] / settings.SCALEFACTOR, pygame.mouse.get_pos()[1] / settings.SCALEFACTOR


def get_pos_raw():
    """
    :return: the mouse pos
    """
    return pygame.mouse.get_pos()


def get_pressed():
    return pygame.mouse.get_pressed()

