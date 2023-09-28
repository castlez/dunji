import random

import pygame

from src.engine import mouse
from src.scenes.base import Scene
from src.settings import Settings as settings
from src.shops.base import Shop

# items
from src.items.candy import Candy
from src.items.cure import Cure
from src.items.gem import Gem
from src.items.hp_pot import HPPot
from src.items.shuriken import Shuriken


class ShopScene(Scene):
    # phase 0 is prep, phase 1 is shop
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

    shop_loc = [(276, 32),
                (351, 107),
                (267, 173)]

    # Player starting positions
    start_pos = [(50, 50), (78, 82), (50, 114)]

    def __init__(self):
        sp = self.start_pos.copy()
        for player in settings.players:
            player.rect.center = sp.pop(0)

        # general ui
        self.img = pygame.image.load("src/sprites/ui/gen_ui.png")
        self.img = pygame.transform.scale(self.img, (settings.WIDTH, settings.HEIGHT))
        settings.players[0].status_location = self.p1_display_pos
        settings.players[1].status_location = self.p2_display_pos
        settings.players[2].status_location = self.p3_display_pos
        self.start_img = pygame.image.load("src/sprites/ui/cbt_start.png")
        self.start_pos = (11, 190)
        self.ind = pygame.image.load("src/sprites/shops/ind.png")

        # get shops
        item_pool = [Candy, Cure, Gem, HPPot, Shuriken]
        self.shops = []
        for loc in self.shop_loc:
            num_items = random.randint(2, 5)
            s = Shop(wares=[random.choice(item_pool)() for _ in range(num_items)],
                     img=pygame.image.load(f"src/sprites/shops/shop_{random.randint(1,3)}.png"),
                     pos=loc)
            self.shops.append(s)


    @staticmethod
    def get_map_icon():
        return pygame.image.load("src/sprites/nav/shops_encounter_icon.png")

    @staticmethod
    def get_description():
        return "Shops"

    def get_info_box_data(self):
        raise NotImplementedError()  # wtf is this?

    def update(self):
        for player in settings.players:
            player.update()
        for shop in self.shops:
            shop.update()
        if self.phase == 0:
            if mouse.get_pressed()[0]:
                m = (mouse.get_pos()[0], mouse.get_pos()[1])
                # checking if start button was pressed
                if self.start_pos[0] < m[0] < self.start_pos[0] + self.start_img.get_width():
                    if self.start_pos[1] + self.start_img.get_height() > m[1] > self.start_pos[1]:
                        # go to the shop phase
                        self.phase = 1
                        print("start")
        elif self.phase == 1:
            # TODO ACTUALLY SHOP
            self.done = True

    def draw(self, screen):
        if self.phase == 0:
            screen.blit(self.start_img, self.start_pos)
        screen.blit(self.img, (0, 0))
        for player in settings.players:
            player.draw_status(screen)
            player.draw(screen)
        for k, shop in enumerate(self.shops):
            shop.draw(screen)
            item_start = self.log_box_pos
            item_step = 34
            if shop.show_wares:
                for i, item in enumerate(shop.wares):
                    screen.blit(item.img,
                                (item_start[0] + item_step*i, item_start[1]))
                    settings.render_text(f"X{item.count}",
                                         (item_start[0] + 20 + item_step*i, item_start[1]))
                screen.blit(self.ind, (self.shop_loc[k][0]-60, self.shop_loc[k][1]-25))
        super().draw(screen)
