import pygame


class Settings:
    # clock stuff
    FRAMERATE = 30

    # screen
    screen = None
    window = None
    WIDTH = 400
    HEIGHT = 300
    SCALEFACTOR = int(1000 / WIDTH)

    # text
    font = None

    # colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (19, 0, 189)
    RED = (140, 0, 0)
    GREEN = (7, 107, 0)
    GREY = (100, 100, 100)

    # state
    chaos = 0
    party_level = 1
    current_scene = None

    # universal values
    combat_speed = 10

    @classmethod
    def initialize(cls):
        cls.screen = pygame.Surface((cls.WIDTH, cls.HEIGHT))
        cls.window = pygame.display.set_mode((cls.WIDTH * cls.SCALEFACTOR, cls.HEIGHT * cls.SCALEFACTOR))
        pygame.display.set_caption("Dunji")
        cls.screen.fill(cls.BLACK)
        cls.font = pygame.font.Font("src/sprites/8bitOperatorPlus8-Regular.ttf", 10 + cls.SCALEFACTOR)
        cls.current_scene = None

    @classmethod
    def render_text(cls, text, pos, size=None, color=WHITE):
        if size:
            f = pygame.font.Font("src/sprites/8bitOperatorPlus8-Regular.ttf", size + cls.SCALEFACTOR)
        else:
            f = cls.font
        cls.screen.blit(f.render(text, True, color), pos)
