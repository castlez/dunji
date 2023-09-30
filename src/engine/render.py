import pygame
from src.settings import Settings as settings


def render_text(text, pos, size=None, color=settings.WHITE):
    if size:
        f = pygame.font.Font("src/sprites/8bitOperatorPlus8-Regular.ttf", size + settings.SCALEFACTOR)
    else:
        f = settings.font
    settings.screen.blit(f.render(text, True, color), pos)
