import pygame


def render_text(text, pos, size=None, color=None, scaled=False):
    from src.settings import Settings as settings
    if color is None:
        color = settings.WHITE
    if size:
        f = pygame.font.Font("src/sprites/8bitOperatorPlus8-Regular.ttf", size + settings.SCALEFACTOR)
    else:
        f = settings.font
    if scaled:
        f = pygame.font.Font("src/sprites/8bitOperatorPlus8-Regular.ttf", size)
        settings.window.blit(f.render(text, False, color),
                             (pos[0]*settings.SCALEFACTOR, pos[1]*settings.SCALEFACTOR))
    else:
        settings.screen.blit(f.render(text, True, color), pos)


def get_text_size(text, size=None, scaled=False):
    from src.settings import Settings as settings
    if size:
        f = pygame.font.Font("src/sprites/8bitOperatorPlus8-Regular.ttf", size + settings.SCALEFACTOR)
    else:
        f = settings.font
    if not scaled:
        return f.size(text)
    else:
        return f.size(text)[0] * settings.SCALEFACTOR, f.size(text)[1] * settings.SCALEFACTOR
