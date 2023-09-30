import random

import pygame

from src.classes.traits.sweet_tooth import SweetTooth
from src.engine import mouse, coords
from src.items.candy import Candy
from src.items.cure import Cure
from src.items.hp_pot import HPPot
from src.items.shuriken import Shuriken
from src.scenes.combat import CombatScene
from src.scenes.map import MapScene
from src.scenes.shops import ShopScene
from src.settings import Settings as settings
from src.engine import render


class Class(pygame.sprite.Sprite):
    def __init__(self,
                 name,
                 hit_die,
                 speed,
                 sprite_img,
                 color,
                 starting_inven,
                 traits):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.hit_die = hit_die
        self.speed = speed
        self.turn_ptr = 0
        self.turn = ["move", "action", "done"]
        self.target = None
        self.traveled = 0  # distance travelled already this turn

        # all classes
        self.level = 1
        self.max_hp = 10 + hit_die
        self.hp = self.max_hp
        self.alive = True

        # static sprits
        self.dead_img = pygame.image.load("src/sprites/grave.png")
        self.trait_img = pygame.image.load("src/sprites/pc/trait_icon.png")
        self.trect = self.trait_img.get_rect()
        self.status_img = pygame.image.load("src/sprites/pc/status_icon.png")
        self.srect = self.status_img.get_rect()
        self.ability_img = pygame.image.load("src/sprites/pc/ability_icon.png")
        self.arect = self.ability_img.get_rect()
        self.inven_img = pygame.image.load("src/sprites/pc/inven_icon.png")
        self.irect = self.inven_img.get_rect()

        self.img = pygame.image.load(f"src/sprites/{sprite_img}").convert_alpha()
        parray = pygame.PixelArray(self.img)
        parray.replace(settings.WHITE, color)
        self.rect = self.img.get_rect()
        self.rect.topleft = (0, 0)

        # player state
        self.status_location = None
        self.traits = traits
        self.statuses = ["todo statuses"]
        self.abilities = ["todo abilities"]
        self.inven = starting_inven  # note: gp is always the first item
        self.show_status = None
        self.done = False

        # shops
        self.current_shop = None
        self.current_order = None  # item to buy

        # number of actions per turn
        # candy increases this by 1
        # reset by player if above 1 after turn
        self.actions = 1

    # General methods

    def draw_status(self, screen):
        screen.blit(self.img, self.status_location)

        # TODO you really shouldnt update pos in draw
        # TODO also these values need tweaking, the click box isnt quite right
        x_off = 13
        y_off = 41
        self.trect.topleft = (self.status_location[0], self.status_location[1] + y_off)
        self.srect.topleft = (self.status_location[0] + x_off, self.status_location[1] + y_off)
        self.arect.topleft = (self.status_location[0] + x_off * 2, self.status_location[1] + y_off)
        self.irect.topleft = (self.status_location[0] + x_off - 4, self.status_location[1] + y_off + 15)

        render.render_text(f"HP: {self.hp}",
                           (self.status_location[0], self.status_location[1] + settings.CELL_SIZE))
        screen.blit(self.trait_img, self.trect.topleft)
        screen.blit(self.status_img, self.srect.topleft)
        screen.blit(self.ability_img, self.arect.topleft)
        screen.blit(self.inven_img, self.irect.topleft)

    def take_damage(self, damage):
        if self.alive:
            self.hp -= damage
            if self.hp <= 0:
                self.die()

    # Abstract methods

    def level_up(self):
        self.level += 1
        self.hp += random.randint(1, self.hit_die)

    def take_turn(self):
        self.use_item()

    def die(self):
        self.alive = False

    @property
    def gold(self):
        return self.inven[0].count

    def pay_gold(self, amount):
        self.inven[0].count -= amount

    def check_traits(self, trait_class):
        for trait in self.traits:
            if type(trait) == trait_class:
                return True
        return False

    def check_items(self, item_class):
        for item in self.inven:
            if type(item) == item_class:
                return True
        return False

    def use_item(self):
        if self.hp + 10 <= self.max_hp and self.check_items(HPPot):
            for item in self.inven:
                if type(item) == HPPot:
                    item.count -= 1
                    self.hp += 10
                    break

        # purge empty items
        new_inven = []
        for item in self.inven:
            if item.count > 0:
                new_inven.append(item)
        self.inven = new_inven

    def update(self):
        # TODO these arent scaling with screen size correctly and
        # TODO are really close together?
        if mouse.get_pressed()[0]:
            m = (mouse.get_pos()[0], mouse.get_pos()[1])
            if self.trect.collidepoint(m):
                self.show_status = "traits"
            elif self.srect.collidepoint(m):
                self.show_status = "statuses"
            elif self.arect.collidepoint(m):
                self.show_status = "abilities"
            elif self.irect.collidepoint(m):
                self.show_status = "inven"
            else:
                # TODO if inven is open and you click a shop it closes :(
                self.show_status = None

    def update_shop(self):
        # if we are in shop scene, shop freely
        # TODO for now: hppot > shuriken > cure > candy
        # for each priority,
        # search shops till you find it
        # then go to that shop
        # TODO repeat until broke i guess?
        if not self.done:
            priority = [HPPot, Shuriken, Cure, Candy]
            if self.check_traits(SweetTooth):
                priority = [Candy, HPPot, Shuriken, Cure]
            if not self.current_shop:
                for p in priority:
                    for s, shop in enumerate(settings.current_scene.shops):
                        if s != settings.current_scene.blacklisted_shop:
                            for item in shop.wares:
                                if type(item) == p:
                                    if item.value <= self.gold:
                                        self.current_shop = shop
                                        self.current_order = item
                                        return
                                    else:
                                        # out of money, so we are done
                                        self.current_shop = None
                                        self.current_order = None
                                        self.done = True
                                        return
                    else:
                        # nothing to buy, done
                        # TODO this is a gross hack to make sure
                        # TODO we dont prematurely end the turn
                        for i, shop in enumerate(settings.current_scene.shops):
                            if settings.current_scene.blacklisted_shop != i:
                                if shop.wares:
                                    break
                        else:
                            self.done = True
                        self.current_shop = None
                        self.current_order = None
            else:
                # go to the shop and buy the item
                for item in self.current_shop.wares:
                    if self.rect.colliderect(self.current_shop):
                        if not self.current_shop.locked:
                            self.current_shop.locked = True
                            self.current_shop.buy_item(self, item)
                            self.current_shop.locked = False
                            self.current_shop = None
                            self.current_order = None
                            break
                        else:
                            self.current_shop = None
                            self.current_order = None
                    else:
                        # not at the shop, so move towards it
                        self.rect.topleft = coords.get_next_pos_towards(self.rect.topleft,
                                                                        self.current_shop.rect.center,
                                                                        settings.combat_speed)
                else:
                    # we were too late, go somewhere else
                    self.current_shop = None
                    self.current_order = None

    def draw(self, screen):
        if type(settings.current_scene) != MapScene:
            if self.alive:
                screen.blit(self.img, self.rect.topleft)
            else:
                screen.blit(self.dead_img, self.rect.topleft)
