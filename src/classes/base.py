import random

import pygame

from src.engine import mouse
from src.scenes.combat import CombatScene
from src.scenes.map import MapScene
from src.scenes.shops import ShopScene
from src.settings import Settings as settings


class Class(pygame.sprite.Sprite):
    def __init__(self, name, hit_die, speed, sprite_img, color, starting_inven):
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
        self.traits = ["todo traits"]
        self.statuses = ["todo statuses"]
        self.abilities = ["todo abilities"]
        self.inven = starting_inven
        self.show_status = None

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
        self.arect.topleft = (self.status_location[0] + x_off*2, self.status_location[1] + y_off)
        self.irect.topleft = (self.status_location[0] + x_off - 4, self.status_location[1] + y_off + 15)

        settings.render_text(f"HP: {self.hp}",
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
        raise NotImplementedError()

    def die(self):
        self.alive = False

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

        # if we are in shop scene, shop freely
        if type(settings.current_scene) == ShopScene:
            pass  # TODO go shopping

    def draw(self, screen):
        if type(settings.current_scene) != MapScene:
            if self.alive:
                screen.blit(self.img, self.rect.topleft)
            else:
                screen.blit(self.dead_img, self.rect.topleft)

