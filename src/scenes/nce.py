import random

import pygame

from src.scenes.base import Scene
from src.scenes.nce_options.beggar import BeggarEvent
from src.settings import Settings as settings


class NCEScene(Scene):
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

    shop_loc = [(256, 12),
                (331, 87),
                (247, 153)]

    # Player starting positions
    start_pos = [(50, 50), (78, 82), (50, 114)]

    @staticmethod
    def get_map_icon():
        return pygame.image.load("src/sprites/nav/non_combat_encounter_icon.png")

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
        self.start_img = pygame.image.load("src/sprites/ui/cbt_start.png")
        self.done_img = pygame.image.load("src/sprites/ui/done.png")
        self.start_pos = (11, 190)
        self.order_locs = [
            (self.p1_display_pos[0], self.p1_display_pos[1] - 20),
            (self.p2_display_pos[0], self.p2_display_pos[1] - 20),
            (self.p3_display_pos[0], self.p3_display_pos[1] - 20)
        ]

        # reset vars
        self.phase = 0
        self.action_order = []

        # encounter itself
        self.encounter = random.choice([
            BeggarEvent(),
        ])

    @staticmethod
    def get_description(floor):
        # TODO maybe do something with floor?
        return "Non-Combat Encounter"

    def update_choose_order(self):
        pass

    def update_go(self):
        pass

    def update(self):
        super().__init__()
        self.encounter.update()
        match self.phase:
            case 0:
                self.update_choose_order()
            case 1:
                self.update_go()
            case 2:
                self.done = True
                return

    def draw_choose_order(self, screen):
        pass

    def draw_go(self, screen):
        pass

    def draw(self, screen):
        screen.blit(self.img, (0, 0))
        for player in settings.players:
            player.draw_status(screen)
            player.draw(screen)
        self.encounter.draw(screen)
        match self.phase:
            case 0:
                self.draw_choose_order(screen)
            case 1:
                self.draw_go(screen)
            case 2:
                pass  # TODO draw outcome
        super().draw(screen)
