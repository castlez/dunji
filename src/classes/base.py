import random
import uuid
import copy

import pygame

from src.classes.traits.giver import Giver
from src.classes.traits.hoarder import Hoarder
from src.classes.traits.hypochondriac import Hypochondriac
from src.classes.traits.sweet_tooth import SweetTooth
from src.engine import mouse, coords
from src.items.base import Item
from src.items.candy import Candy
from src.items.coins import Coins
from src.items.cure import Cure
from src.items.gem import Gem
from src.items.hp_pot import HPPot
from src.items.shuriken import Shuriken
from src.scenes.map import MapScene
from src.settings import Settings as settings
from src.engine import render
from src.statuses.base import Status
from src.statuses.confused import Confused


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
        self.color = color
        self.hit_die = hit_die
        self.base_speed = speed
        self.speed = speed
        self.base_actions = 1
        self.actions = 1
        self.turn_ptr = 0
        self.turn = ["move", "action", "done"]
        self.target = None
        self.traveled = 0  # distance travelled already this turn

        # all classes
        self.level = 1
        self.max_hp = 10 + hit_die
        self.hp = self.max_hp
        self.alive = True

        # lambda functions for bonus damage
        self.bonus_damage = None
        self.bonus_damage_taken = None

        # unique id
        self.id = str(uuid.uuid4()).split("-")[0]

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
        self.statuses: list[Status] = []
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
            if self.bonus_damage_taken:
                damage = self.bonus_damage_taken(damage)
            self.hp -= damage
            settings.log.bad(f"took {damage} damage!", self)
            if self.hp <= 0:
                self.die()

    # Abstract methods

    def level_up(self):
        self.level += 1
        self.hp += random.randint(1, self.hit_die)

    def take_turn(self):
        raise NotImplementedError()

    def get_closest_valid_target(self):
        # find the closest enemy
        closest = None
        targets = settings.current_scene.enemies
        if self.check_statuses(Confused):
            if random.randint(0, 20) > 10:
                targets = settings.current_scene.enemies + [p for p in settings.players if p != self]
        if targets:
            closest = targets[0]
            for enemy in targets:
                if enemy.alive:
                    dist_to_enemy = coords.distance(self.rect.topleft, enemy.rect.topleft)
                    dist_to_closest = coords.distance(self.rect.topleft, closest.rect.topleft)
                    if not closest:
                        closest = enemy
                    elif dist_to_enemy < dist_to_closest:
                        closest = enemy
        return closest

    def start_turn(self):
        settings.log.info("starts their turn.", self)
        self.use_item()
        self.do_statuses()

    def rest(self):
        self.hp = self.max_hp
        self.actions = 1

    def do_statuses(self):
        for status in self.statuses:
            status.enact()

        new_statuses = []
        for status in self.statuses:
            if status.duration > 0:
                new_statuses.append(status)
        self.statuses = new_statuses

    def check_statuses(self, status_class):
        for status in self.statuses:
            if type(status) == status_class:
                return True
        return False

    def die(self):
        settings.log.bad("has died!", self)
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
        for player in settings.players:
            if player.check_traits(Giver):
                avail_items = self.inven + player.inven
                break
        else:
            avail_items = self.inven

        # use the next item that makes sense
        # this is technically a priority list right now
        # since the loop breaks after item use, i think that's ok
        used_item: Item = None  # noqa
        for item in avail_items:
            if type(item) == Gem or type(item) == Coins:
                continue
            # Health Potion
            if self.hp + 10 <= self.max_hp or \
                    (self.check_traits(Hypochondriac) and self.hp < self.max_hp):
                if type(item) == HPPot:
                    used_item = item
                    break
            # Cure
            if self.statuses:
                if type(item) == Cure:
                    item.use(self)
                    used_item = item
                    break

            # Candy
            if type(item) == Candy:
                item.use(self)
                used_item = item
                break

            # Shuriken
            if type(item) == Shuriken:
                # only one shuriken at a time cuz im shit
                for obj in settings.current_scene.objects:
                    if type(obj) == Shuriken:
                        break
                else:
                    item.use(self.get_closest_valid_target())
                    item.rect.topleft = self.rect.topleft
                    settings.current_scene.objects.append(item)
                    used_item = item
                    break

        # update item count and log
        if used_item:
            used_item.count -= 1
            settings.log.good(f"used {used_item.name}.", self)

    def update(self):
        # update inventory
        new_inven = [self.inven[0]]  # pre-add gold
        for item in self.inven[1:]:
            if item.count > 0:
                new_inven.append(item)
        self.inven = new_inven
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
                            # sell all gems
                            for player_item in self.inven:
                                if type(player_item) == Gem:
                                    if not self.check_traits(Hoarder):
                                        self.inven[0].count += player_item.value * player_item.count
                                        player_item.count = 0

                            self.current_shop.locked = True
                            self.current_shop.buy_item(self, item)
                            self.current_shop.locked = False

                            # reset
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
