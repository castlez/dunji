import random

import pygame

from src.classes.traits.peace_keeper import PeaceKeeper
from src.engine import mouse
from src.scenes.base import Scene
from src.settings import Settings as settings
from src.shops.base import Shop
from src.engine import render


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
    blacklist_prompt_pos = (145, 92)

    log_box_pos = (200, 230)

    shop_loc = [(256, 12),
                (331, 87),
                (247, 153)]

    # Player starting positions
    start_pos = [(50, 50), (78, 82), (50, 114)]

    def __init__(self):
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
        self.ind = pygame.image.load("src/sprites/shops/ind.png")

        # get shops (gems cant show up as wares)
        item_pool = [Candy, Cure, HPPot, Shuriken]
        self.shops = []
        for loc in self.shop_loc:
            num_items = random.randint(2, 5)
            s = Shop(wares=[random.choice(item_pool)() for _ in range(num_items)],
                     img=pygame.image.load(f"src/sprites/shops/shop_{random.randint(1,3)}.png"),
                     pos=loc)
            self.shops.append(s)

        # what we are hovering over
        self.hover = None

        # blacklist

        # index of blacklisted shop in self.shops
        self.blacklisted_shop = None
        self.blacklist_img = pygame.image.load("src/sprites/shops/blacklist.png")

    @staticmethod
    def get_map_icon():
        return pygame.image.load("src/sprites/nav/shops_encounter_icon.png")

    @staticmethod
    def get_description(floor):
        # TODO do something with the floor this shop is on
        return ["Shops"]

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
                        return
                # check if a shop was blacklisted
                for i, shop in enumerate(self.shops):
                    if shop.rect.collidepoint(m):
                        self.blacklisted_shop = i
        elif self.phase == 1:
            # TODO ACTUALLY SHOP
            for player in settings.players:
                if not player.done:
                    break
            else:
                self.phase = 2
                return
            for player in settings.players:
                player.update_shop()
        elif self.phase == 2:
            for player in settings.players:
                if player.get_traits(PeaceKeeper):
                    settings.chaos = settings.chaos - 1 if settings.chaos > 0 else 0
            if mouse.get_pressed()[0]:
                m = (mouse.get_pos()[0], mouse.get_pos()[1])
                # checking if start button was pressed
                if self.start_pos[0] < m[0] < self.start_pos[0] + self.start_img.get_width():
                    if self.start_pos[1] + self.start_img.get_height() > m[1] > self.start_pos[1]:
                        # reset and dip
                        self.phase = 0
                        self.blacklisted_shop = None
                        self.done = True
                        return

        # check if we are hovering over a shops wares
        for shop in self.shops:
            if shop.show_wares:
                for item in shop.wares:
                    if item.rect.collidepoint(mouse.get_pos()):
                        self.hover = item
                        return
        self.hover = None

    def draw(self, screen):
        screen.blit(self.img, (0, 0))
        for player in settings.players:
            player.draw_status(screen)
            player.draw(screen)
        for k, shop in enumerate(self.shops):
            shop.draw(screen)
            item_start = self.log_box_pos
            item_step = 34

            # draw x over blacklisted shop
            if self.blacklisted_shop == k:
                screen.blit(self.blacklist_img, (shop.rect.center[0] - 20, shop.rect.center[1] - 20))

            if shop.show_wares:
                for i, item in enumerate(shop.wares):
                    p = (item_start[0] + item_step*i, item_start[1])
                    item.rect.topleft = p
                    screen.blit(item.img,
                                (item_start[0] + item_step*i, item_start[1]))
                    render.render_text(f"X{item.count}",
                                         (item_start[0] + 20 + item_step*i, item_start[1]))
                    if self.hover == item:
                        hover_pos = (self.log_box_pos[0] - 3, self.log_box_pos[1] - 15)
                        render.render_text(f"{item.name} - {item.description}",
                                           hover_pos)
                screen.blit(self.ind, (self.shop_loc[k][0]-35, self.shop_loc[k][1] + 14))
            if self.phase == 0:
                screen.blit(self.start_img, self.start_pos)
                if self.blacklisted_shop is None:
                    render.render_text("Blacklist 1 shop", self.blacklist_prompt_pos)
            if self.phase == 2:
                screen.blit(self.done_img, self.start_pos)
                render.render_text("Click done to continue", self.blacklist_prompt_pos)
            super().draw(screen)
