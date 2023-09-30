import pygame


def render_text(text, pos, size=None, color=None):
    from src.settings import Settings as settings
    if color is None:
        color = settings.WHITE
    if size:
        f = pygame.font.Font("src/sprites/8bitOperatorPlus8-Regular.ttf", size + settings.SCALEFACTOR)
    else:
        f = settings.font
    settings.screen.blit(f.render(text, True, color), pos)


def get_text_size(text, size=None):
    from src.settings import Settings as settings
    if size:
        f = pygame.font.Font("src/sprites/8bitOperatorPlus8-Regular.ttf", size + settings.SCALEFACTOR)
    else:
        f = settings.font
    return f.size(text)
