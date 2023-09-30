import random

import pygame

from src.scenes.base import Scene
from src.settings import Settings as settings
from src.engine import mouse
from src.engine import render


# scenes
from src.scenes.combat import CombatScene
from src.scenes.shops import ShopScene


class MapOption(pygame.sprite.Sprite):
    def __init__(self, scene, floor):
        pygame.sprite.Sprite.__init__(self)
        self.img = scene.get_map_icon()
        self.img_d = scene.get_map_icon()
        self.rect = self.img.get_rect()
        self.desc_lines = scene.get_description()
        self.floor = floor
        self.scene = scene

    def place(self, x, y):
        self.rect.topleft = (x, y)

    def update(self):
        pass

    def draw(self, screen):
        if self.floor != settings.current_floor:
            dark = pygame.Surface((self.img_d.get_width(), self.img_d.get_height()), flags=pygame.SRCALPHA)
            dark.fill((50, 50, 50, 0))
            self.img_d.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            screen.blit(self.img_d, self.rect.topleft)
        else:
            screen.blit(self.img, self.rect.topleft)


class MapScene(Scene):
    # screen locations
    info_box_pos = (159, 80)
    status_x = 100
    start = 40
    step = 80
    p1_display_pos = (status_x, start)
    p2_display_pos = (status_x, start + step)
    p3_display_pos = (status_x, start + step * 2)

    # map locations
    start_x = 180
    start_y = 240
    step = 50
    rows = [(start_x, start_y),
            (start_x, start_y - step),
            (start_x, start_y - step * 2),
            (start_x, start_y - step * 3),
            (start_x, start_y - step * 4)]
    start_y_label = 250
    floor_labels = [(start_x - 20, start_y_label),
                    (start_x - 20, start_y_label - step),
                    (start_x - 20, start_y_label - step * 2),
                    (start_x - 20, start_y_label - step * 3),
                    (start_x - 20, start_y_label - step * 4)]

    def __init__(self):
        self.img = pygame.image.load("src/sprites/ui/map_back.png")

        settings.players[0].status_location = self.p1_display_pos
        settings.players[1].status_location = self.p2_display_pos
        settings.players[2].status_location = self.p3_display_pos

        # build map if we dont have one
        if not settings.map:
            self.build_map()

        for i, row in enumerate(settings.map):
            for j, scene in enumerate(row):
                num_opts = len(row)
                x = self.rows[i][0] + 50 * j
                y = self.rows[i][1]
                match num_opts:
                    case 2:
                        x += 50
                    case 3:
                        x += 25
                    case 1:
                        x += 75
                scene.place(x, y)

    def update(self):
        for player in settings.players:
            player.update()
        # check if dm has selected a map
        if mouse.get_pressed()[0]:
            # check if we clicked a map option
            for row in settings.map:
                for opt in row:
                    if opt.rect.collidepoint(mouse.get_pos()):
                        if opt.floor == settings.current_floor:
                            settings.current_scene = opt.scene()

    def draw(self, screen):
        screen.blit(self.img, (0, 0))
        for p in settings.players:
            p.draw_status(screen)

        # draw map icons
        for i, row in enumerate(settings.map):
            if i < settings.current_floor:
                color = settings.BLACK
            elif i == settings.current_floor:
                color = settings.RED
            else:
                color = settings.WHITE
            render.render_text(f"F{i+1}", self.floor_labels[i], color=color)
            for j, scene in enumerate(row):
                scene.draw(screen)

        # draw scene description if we hover over a map option
        for row in settings.map:
            for opt in row:
                if opt.rect.collidepoint(mouse.get_pos()):
                    for i, line in enumerate(opt.desc_lines):
                        y_offset = 30 * len(opt.desc_lines)
                        render.render_text(line, (mouse.get_pos()[0], mouse.get_pos()[1] - y_offset + 20 * i))
        super().draw(screen)


    @staticmethod
    def build_map():
        """
        Generate a map if there isn't one already

        [
        [floor 1 options],
        [floor 2 options],
        [floor 3 options],
        [floor 4 options],
        [boss encounter (maybe not always combat?)]
        ]

        Drawn in reverse so you travel up
        :return:
        """
        scene_types = [CombatScene, ShopScene]

        # the first three floors can have anything
        for i in range(3):
            floors = random.randint(2, 4)  # either 2 or 3 floors
            settings.map.append([MapOption(random.choice(scene_types), i) for _ in range(floors)])

        # the fourth floor is always a choice between a town and combat
        # TODO add town scene
        # settings.map.append([random.choice([CombatScene, TownScene])])
        settings.map.append([MapOption(CombatScene, 3), MapOption(ShopScene, 3)])

        # boss encounter
        # TODO add boss scene
        settings.map.append([MapOption(CombatScene, 4)])
