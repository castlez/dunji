import pygame

from src.log import Log
from src.engine import render

class Settings:
    # clock stuff
    FRAMERATE = 30

    # screen
    screen = None
    window = None
    WIDTH = 400
    HEIGHT = 300
    SCALEFACTOR = 2.5
    CELL_SIZE = 32

    # text
    font = None

    # colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (19, 0, 189)
    RED = (140, 0, 0)
    BRED = (255, 17, 0)
    GREEN = (7, 107, 0)
    BGREEN = (0, 255, 0)
    BROWN = (107, 71, 0)
    BBROWN = (220, 120, 0)
    YELLOW = (255, 255, 0)
    GREY = (100, 100, 100)

    # state
    players = []
    chaos = 1
    party_level = 1
    current_scene = None
    current_scene_name = None
    map = []  # multi-dimensional array of scenes
    current_floor = 0  # current floor INDEX
    base_cr = 3
    session = 1


    # combat
    combat_speed = 10
    fast_play = False  # go to next turn without waiting for user input

    # log
    log = None

    # events per frame
    events = []

    # game
    session_boss_option = None

    @classmethod
    def get_floor_mod(cls, floor):
        return floor + (5 * (cls.session - 1))

    @classmethod
    def get_collidables(cls):
        collidables = []
        for player in cls.players:
            collidables.append(player)
        for enemy in cls.current_scene.enemies:
            collidables.append(enemy)
        return collidables

    @classmethod
    def initialize(cls):
        cls.screen = pygame.Surface((cls.WIDTH, cls.HEIGHT))
        cls.window = pygame.display.set_mode((cls.WIDTH * cls.SCALEFACTOR, cls.HEIGHT * cls.SCALEFACTOR))
        pygame.display.set_caption("Dunji")
        cls.screen.fill(cls.BLACK)
        cls.font = pygame.font.Font("src/sprites/8bitOperatorPlus8-Regular.ttf", int(10 + cls.SCALEFACTOR))
        cls.current_scene = None
