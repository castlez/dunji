import random

import pygame

from src.classes.traits.peace_keeper import PeaceKeeper
from src.classes.witch import Witch
from src.engine import mouse
from src.items.coins import Coins
from src.scenes.base import Scene
from src.scenes.map import MapScene
from src.settings import Settings as settings
from src.shops.base import Shop
from src.engine import render


# items
from src.items.candy import Candy
from src.items.cure import Cure
from src.items.gem import Gem
from src.items.hp_pot import HPPot
from src.items.shuriken import Shuriken

# import all traits from the traits folder
from src.classes.traits.clepto import Clepto
from src.classes.traits.giver import Giver
from src.classes.traits.hoarder import Hoarder
from src.classes.traits.hypochondriac import Hypochondriac
from src.classes.traits.sweet_tooth import SweetTooth
from src.classes.traits.peace_keeper import PeaceKeeper
from src.classes.traits.sneaky import Sneaky


class PlayerSelect:
    class_pool = [
        Witch
    ]

    item_pool = [
        HPPot,
        Shuriken,
        Gem,
        Candy,
        Cure
    ]

    trait_pool = [
        Clepto,
        Giver,
        Hoarder,
        Hypochondriac,
        SweetTooth,
        PeaceKeeper,
        Sneaky
    ]

    def __init__(self, color, pos):
        # player select locations
        self.pos = pos
        self.left_img = pygame.image.load("src/sprites/shops/ind.png")
        self.left_img = pygame.transform.rotate(self.left_img, 180)
        self.left_rect = self.left_img.get_rect()
        self.left_rect.topleft = (self.pos[0] - 30, self.pos[1])
        self.right_img = pygame.image.load("src/sprites/shops/ind.png")
        self.right_rect = self.right_img.get_rect()
        self.right_rect.topleft = (self.pos[0] + 30, self.pos[1])
        self.desc_img = pygame.image.load("src/sprites/ui/vert.png")
        self.desc_rect = self.desc_img.get_rect()
        self.desc_rect.topleft = (self.pos[0] - 26, self.pos[1] + 32)
        self.desc_img = pygame.transform.scale(self.desc_img, (84, 170))
        self.color = color
        self.title_pos = (self.pos[0], self.pos[1] - 15)
        self.info_img = pygame.image.load("src/sprites/ui/vert.png")
        self.info_img = pygame.transform.scale(self.info_img, (100, 60))
        self.info_rect = self.info_img.get_rect()
        self.show_aspect = None
        self.mouse_down = False

        # generate player choices
        self.choices = []
        for i in range(3):
            self.choices.append(self.generate_player())

        self.current_choice = 0

    def generate_player(self):
        # generate player
        player = random.choice(self.class_pool)(color=self.color,
                                                starting_inven=[],
                                                traits=[])
        # starting gold
        player.inven.append(Coins())
        player.inven[0].count = random.randint(20, 40)
        player.inven[0].img = pygame.transform.scale(player.inven[0].img,
                                                     (8, 8))

        # starting item
        player.inven.append(random.choice(self.item_pool)())

        # generate traits
        for i in range(random.randint(0, 2)):
            player.traits.append(random.choice(self.trait_pool)())

        # set status location
        player.status_location = self.pos
        return player

    def update(self):
        m = mouse.get_pos()
        if mouse.get_pressed()[0]:
            if not self.mouse_down:
                if self.left_rect.collidepoint(m):
                    self.current_choice -= 1
                    if self.current_choice < 0:
                        self.current_choice = len(self.choices) - 1
                elif self.right_rect.collidepoint(m):
                    self.current_choice += 1
                    if self.current_choice > len(self.choices) - 1:
                        self.current_choice = 0
            self.mouse_down = True
        else:
            self.mouse_down = False

    def draw(self, screen):
        screen.blit(self.left_img, self.left_rect.topleft)
        screen.blit(self.right_img, self.right_rect.topleft)
        self.choices[self.current_choice].draw_status(screen)

        # draw description
        screen.blit(self.desc_img, self.desc_rect.topleft)
        render.render_text("Traits | Items",
                           (self.pos[0] - 26, self.pos[1] + 38),
                           color=settings.BLACK)
        render.render_text(self.choices[self.current_choice].name,
                           self.title_pos)
        start = (self.pos[0] - 24, self.pos[1] + 48)
        step = 34
        m = mouse.get_pos()
        new_show = None
        # check for hover on trait
        for i, trait in enumerate(self.choices[self.current_choice].traits):
            trait.rect.topleft = (start[0], start[1] + step * i)
            screen.blit(trait.img, trait.rect.topleft)
            if trait.rect.collidepoint(m):
                new_show = trait

        # check for hover on item
        for i, item in enumerate(self.choices[self.current_choice].inven):
            item.rect.topleft = (start[0] + 50, start[1] + step * i)
            if i == 0:
                p = item.rect
                screen.blit(item.img, (p.topleft[0], p.topleft[1] + 8))
                # draw gold count
                render.render_text(f"X{item.count}",
                                   (start[0] + 60, start[1] + 8))
            else:
                screen.blit(item.img, item.rect.topleft)

            if item.rect.collidepoint(m):
                new_show = item
        self.show_aspect = new_show


class PartySelectScene(Scene):

    def __init__(self):
        start = (80, 40)
        step = 100
        locs = [
            (start[0], start[1]),
            (start[0] + step, start[1]),
            (start[0] + step * 2, start[1])
        ]
        self.choices = [
            PlayerSelect(settings.RED, locs[0]),
            PlayerSelect(settings.BLUE, locs[1]),
            PlayerSelect(settings.GREEN, locs[2])
        ]
        self.start_img = pygame.image.load("src/sprites/ui/cbt_start.png")
        self.start_rect = self.start_img.get_rect()
        self.start_rect.center = (settings.WIDTH // 2, settings.HEIGHT - 30)

    @staticmethod
    def get_map_icon():
        pass  # no op

    def update(self):
        for select in self.choices:
            select.update()
        if mouse.get_pressed()[0]:
            m = (mouse.get_pos()[0], mouse.get_pos()[1])
            # checking if start button was pressed
            if self.start_rect.collidepoint(m):
                settings.players = []
                for select in self.choices:
                    settings.players.append(select.choices[select.current_choice])
                settings.current_scene = MapScene()
                self.done = True

    def draw(self, screen):
        m = mouse.get_pos()
        for choice in self.choices:
            choice.draw(screen)

        for choice in self.choices:
            if choice.show_aspect:
                dsize = render.get_text_size(choice.show_aspect.description)
                new_size = (dsize[0], dsize[1] * 2 + 5)
                new_loc = (m[0] + 10, m[1] + 10)
                choice.info_img = pygame.transform.scale(choice.info_img,
                                                         new_size)
                if new_loc[0] + choice.info_img.get_width() > settings.WIDTH:
                    new_loc = (new_loc[0] - choice.info_img.get_width() - 20,
                               new_loc[1])
                choice.info_rect.topleft = new_loc
                screen.blit(choice.info_img, choice.info_rect.topleft)
                render.render_text(choice.show_aspect.name,
                                   new_loc)
                render.render_text(choice.show_aspect.description,
                                   (new_loc[0], new_loc[1] + 10))

        # start button
        screen.blit(self.start_img, self.start_rect.topleft)