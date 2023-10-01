import random

import pygame

from src.engine import render, mouse
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
    start_pos = [(50, 100), (78, 132), (50, 164)]

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
        self.player_rects = [
            pygame.Rect(self.p1_display_pos, (settings.CELL_SIZE, settings.CELL_SIZE)),
            pygame.Rect(self.p2_display_pos, (settings.CELL_SIZE, settings.CELL_SIZE)),
            pygame.Rect(self.p3_display_pos, (settings.CELL_SIZE, settings.CELL_SIZE)),
        ]
        self.start_img = pygame.image.load("src/sprites/ui/cbt_start.png")
        self.start_rect = self.start_img.get_rect()
        self.start_rect.topleft = (128.0, 186.8)
        self.done_img = pygame.image.load("src/sprites/ui/done.png")
        self.done_rect = self.done_img.get_rect()
        self.done_rect.topleft = (128.0, 186.8)
        self.outcome_box_img = pygame.image.load("src/sprites/ui/vert2.png")
        self.outcome_box_img = pygame.transform.scale(self.outcome_box_img,
                                                      (200, 100))
        self.outcome_box_rect = self.outcome_box_img.get_rect()
        self.outcome_box_rect.topleft = (148.8, 17.6)

        x_off = 12
        y_off = -16
        self.order_locs = [
            (self.start_pos[0][0] + x_off, self.start_pos[0][1] + y_off),
            (self.start_pos[1][0] + x_off, self.start_pos[1][1] + y_off),
            (self.start_pos[2][0] + x_off, self.start_pos[2][1] + y_off),
        ]
        self.instructions_pos = (5, self.log_pos[1] - 16)

        # reset vars
        self.phase = 0
        self.action_order = []  # order the players go it

        # encounter itself
        self.encounter = random.choice([
            BeggarEvent(),
        ])

        self.votes = [-1, -1, -1]

    @staticmethod
    def get_description(floor):
        # TODO maybe do something with floor?
        return ["Non-Combat Encounter"]

    def update_choose_order(self):
        m = mouse.get_pos()
        if mouse.get_pressed()[0]:
            for i, player in enumerate(settings.players):
                if self.player_rects[i].collidepoint(m):
                    if player not in self.action_order:
                        self.action_order.append(player)
            if self.start_rect.collidepoint(m):
                if len(self.action_order) == 3:
                    self.phase = 1
                    return

    def update_go(self):
        for i, player in enumerate(self.action_order):
            self.votes[i] = self.encounter.get_vote(player)
        self.phase = 2

    def update(self):
        super().__init__()
        self.encounter.update()
        match self.phase:
            case 0:
                self.update_choose_order()
            case 1:
                self.update_go()
            case 2:
                if not self.encounter.done:
                    self.encounter.check_resolve(self.action_order[0])
                if not self.encounter.done:
                    # first voter didn't resolve the encounter
                    # so time to vote
                    results = [0, 0, 0]
                    for i, player in enumerate(self.action_order):
                        results[self.votes[i]] += 1
                        if i == 0:
                            results[self.votes[i]] += 0.5
                    choice = results.index(max(results))
                    self.encounter.resolve(choice)

                # rescale outcome box
                size_x = render.get_text_size(self.encounter.choices[self.encounter.final_choice])[0] - 60
                self.outcome_box_img = pygame.transform.scale(self.outcome_box_img, (size_x, self.outcome_box_rect.height))
                self.outcome_box_rect = self.outcome_box_img.get_rect()
                self.outcome_box_rect.topleft = (settings.WIDTH - size_x - 5, self.outcome_box_rect.top + 6)

                # done button
                if self.done_rect.collidepoint(mouse.get_pos()):
                    if mouse.get_pressed()[0]:
                        self.done = True

    def draw_choose_order(self, screen):
        render.render_text("Choose a voting order by clicking slimes in the info box", self.instructions_pos)
        screen.blit(self.start_img, self.start_rect.topleft)

    def draw_go(self, screen):
        pass

    def draw_outcome(self, screen):
        screen.blit(self.outcome_box_img, self.outcome_box_rect.topleft)
        screen.blit(self.done_img, self.done_rect.topleft)

        # write results to outcome box
        render.render_text(f"{self.encounter.name}", (self.outcome_box_rect.left + 5, self.outcome_box_rect.top + 5))
        render.render_text(f"Outcome chosen:",
                           (self.outcome_box_rect.left + 5, self.outcome_box_rect.top + 20))
        parts = self.encounter.choices[self.encounter.final_choice].split(')', 1)
        outcome = parts[1]
        render.render_text(outcome,
                           (self.outcome_box_rect.left, self.outcome_box_rect.top + 30))

    def draw(self, screen):
        screen.blit(self.img, (0, 0))
        for i, player in enumerate(settings.players):
            player.draw_status(screen)
            player.draw(screen)
            if player in self.action_order:
                render.render_text(f"{self.action_order.index(player) + 1}", self.order_locs[i])
        self.encounter.draw(screen)
        match self.phase:
            case 0:
                self.draw_choose_order(screen)
            case 1:
                self.draw_go(screen)
            case 2:
                if self.encounter.done:
                    self.draw_outcome(screen)
        super().draw(screen)
