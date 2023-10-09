import random

import pygame

from src.engine import render, mouse, keys
from src.scenes.base import Scene
from src.scenes.boss_options.lich import LichEvent
from src.settings import Settings as settings


class BossScene(Scene):
    # Non-Combat Encounter
    # phase 0 is pick action order, phase 1 is go, phase 2 is outcome
    phase = 0

    # screen locations
    player_screen_start = (12, 230)
    status_screen_start = (200, 230)
    status_y = 225
    p1_display_pos = (22, status_y)
    p2_display_pos = (82, status_y)
    p3_display_pos = (142, status_y)
    info_box_pos = (20, 20)

    log_box_pos = (200, 230)

    # Player starting positions
    start_pos = [(50, 100), (78, 132), (50, 164)]

    enemies = []  # in case there is combat

    @staticmethod
    def get_map_icon():
        return settings.session_boss_option.get_map_icon()

    def __init__(self):
        super().__init__()

        sp = self.start_pos.copy()
        for player in settings.players:
            player.rect.topleft = sp.pop(0)
            player.done = False

        # general ui
        self.img = pygame.image.load("src/sprites/ui/gen_ui.png")
        self.img = pygame.transform.scale(self.img, (settings.WIDTH, settings.HEIGHT))

        settings.players[0].status_location = self.p1_display_pos
        settings.players[1].status_location = self.p2_display_pos
        settings.players[2].status_location = self.p3_display_pos
        self.player_rects = [
            pygame.Rect(self.p1_display_pos, (settings.CELL_SIZE, settings.CELL_SIZE)),
            pygame.Rect(self.p2_display_pos, (settings.CELL_SIZE, settings.CELL_SIZE)),
            pygame.Rect(self.p3_display_pos, (settings.CELL_SIZE, settings.CELL_SIZE)),
        ]

        self.outcome_box_img = pygame.image.load("src/sprites/ui/vert2.png")
        self.outcome_box_img = pygame.transform.scale(self.outcome_box_img,
                                                      (200, 100))
        self.outcome_box_rect = self.outcome_box_img.get_rect()
        self.outcome_box_rect.topleft = (148.8, 17.6)

        settings.log.set_pos((self.log_box_pos[0] - 5,
                              self.log_box_pos[1] - 5))

        # reset vars
        self.phase = 0
        self.is_turn = False

        # encounter itself
        self.objects = []

    @staticmethod
    def get_description(floor):
        # TODO maybe do something with floor?
        return ["Boss Encounter"]

    def draw_outcome(self, screen):
        pass

    def update(self):
        match self.phase:
            case 0:
                settings.session_boss_option.update()
            case 1:
                settings.session_boss_option.update()
            case 2:
                self.done = True

    def draw(self, screen):
        screen.blit(self.img, (0, 0))
        settings.session_boss_option.draw(screen)
        if settings.session_boss_option.done:
            self.draw_outcome(screen)
        super().draw(screen)
