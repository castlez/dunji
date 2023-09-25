import random

import pygame


class Class(pygame.sprite.Sprite):
    def __init__(self, name, hit_die, speed):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.hit_die = hit_die
        self.speed = speed
        self.turn_ptr = 0
        self.turn = ["move", "action", "done"]

        # all classes
        self.level = 1
        self.hp = 10 + hit_die
        self.pos = None
        self.alive = True
        self.dead_img = pygame.image.load("src/sprites/grave.png")

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

