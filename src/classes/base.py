import random

import pygame

from src.settings import Settings as settings


class Class(pygame.sprite.Sprite):
    def __init__(self, name, hit_die, speed, sprite_img, color):
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

        # static sprits
        self.dead_img = pygame.image.load("src/sprites/grave.png")
        self.trait_img = pygame.image.load("src/sprites/pc/trait_icon.png")
        self.status_img = pygame.image.load("src/sprites/pc/status_icon.png")
        self.ability_img = pygame.image.load("src/sprites/pc/ability_icon.png")
        self.inven_img = pygame.image.load("src/sprites/pc/inven_icon.png")

        self.img = pygame.image.load(f"src/sprites/{sprite_img}").convert_alpha()
        parray = pygame.PixelArray(self.img)
        parray.replace(settings.WHITE, color)
        self.rect = self.img.get_rect()
        self.rect.center = (0, 0)

        self.status_location = None
        self.traits = ["todo traits"]
        self.statuses = ["todo statuses"]

    # General methods

    def draw_status(self, screen):
        screen.blit(self.img, self.status_location)
        settings.render_text(f"HP: {self.hp}",
                             (self.status_location[0], self.status_location[1] + settings.CELL_SIZE))
        screen.blit(self.trait_img, (self.status_location[0] - 12, self.status_location[1] + 30))
        screen.blit(self.status_img, (self.status_location[0], self.status_location[1] + 30))
        screen.blit(self.ability_img, (self.status_location[0] + 12, self.status_location[1] + 30))
        screen.blit(self.inven_img, (self.status_location[0], self.status_location[1] + 40))

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

    def draw(self, screen):
        if self.alive:
            screen.blit(self.img, self.rect.center)
        else:
            screen.blit(self.dead_img, self.rect.center)

