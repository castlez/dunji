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


def get_pressed(up=True):
    for event in settings.events:
        if up:
            if event.type == pygame.MOUSEBUTTONUP:
                return 1, 0
            return 0, 0
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return 1, 0
            return 0, 0
    return 0, 0


def get_held():
    return pygame.mouse.get_pressed()

