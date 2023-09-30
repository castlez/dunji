import math

import pygame

from src.classes.traits.sneaky import Sneaky
from src.engine import coords
from src.settings import Settings as settings


class Enemy(pygame.sprite.Sprite):
    # used for enemy placement
    sprite_img = None  # list of sprite layers
    cr = 0  # challenge rating

    def __init__(self, pos, name, hp, damage, speed, description, sprite_img):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.description = description
        self.img = pygame.image.load(f"src/sprites/{sprite_img}").convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.topleft = pos

        # edit color of enemy for spice
        parray = pygame.PixelArray(self.img)
        # TODO do better coloring of enemies
        parray.replace(settings.WHITE, settings.GREY)

        self.turn_ptr = 0
        self.turn = ["move", "action", "done"]
        self.target = None
        self.traveled = 0  # distance travelled already this turn

        self.statuses = []

        self.alive = True

    def take_turn(self):
        self.do_statuses()

    def do_statuses(self):
        for status in self.statuses:
            status.enact()

        new_statuses = []
        for status in self.statuses:
            if status.duration > 0:
                new_statuses.append(status)
        self.statuses = new_statuses

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()

    def die(self):
        self.alive = False
        self.kill()

    def draw(self, screen):
        if not self.img:
            raise Exception("fuck 1")
        screen.blit(self.img, self.rect.topleft)

    def move(self, pos):
        # TODO do i need both of these?
        self.rect.topleft = pos

    def move_towards(self, dest):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = dest[0] - self.rect.topleft[0], dest[1] - self.rect.topleft[1]
        dist = math.hypot(dx, dy)
        stopped = False
        if self.traveled + settings.combat_speed > self.speed:
            if dist - self.speed > 0:
                stopped = True
        dx, dy = dx / dist, dy / dist  # Normalize
        # Move along this normalized vector towards the player
        pos = (self.rect.topleft[0] + dx * settings.combat_speed, self.rect.topleft[1] + dy * settings.combat_speed)
        self.move(pos)
        self.traveled += settings.combat_speed
        return stopped

    def in_melee(self, target):
        return coords.distance(self.rect.topleft, target.rect.topleft) <= 10

    def get_target(self):
        closest = None
        for player in settings.players:
            if player.hp > 0:
                if not player.check_traits(Sneaky) or len([p for p in settings.players if p.alive]) == 1:
                    if not closest:
                        closest = player
                    elif coords.distance(self.rect.topleft, player.rect.topleft) < \
                            coords.distance(self.rect.topleft,
                                            closest.rect.topleft):

                        closest = player
        return closest
