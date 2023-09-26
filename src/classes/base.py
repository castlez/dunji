import random

import pygame

from src.settings import Settings as settings


class Class(pygame.sprite.Sprite):
    def __init__(self, name, hit_die, speed, sprite_layers, color):
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
        self.hp = 10 + hit_die
        self.alive = True
        self.dead_img = pygame.image.load("src/sprites/grave.png")

        self.img_base = pygame.image.load("src/sprites/slime_base.png").convert_alpha()
        parray = pygame.PixelArray(self.img_base)
        parray.replace(settings.WHITE, color)
        self.img_over = pygame.image.load("src/sprites/pc/witch_over.png")
        self.rect = self.img_base.get_rect()
        self.rect.center = (0, 0)

    # General methods

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

