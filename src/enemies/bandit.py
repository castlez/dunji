import math

import pygame.image

from src.enemies.base import Enemy
from src.settings import Settings as settings


class Bandit(Enemy):
    # used for enemy placement
    sprite_layers = ["slime_base.png", "baddies/bandit_over.png"]
    cr = 1

    def __init__(self, pos):
        super().__init__(pos=pos,
                         name="Bandit",
                         hp=5,
                         damage=2,
                         speed=9,
                         description="A bandit. He's not very nice.")
        self.img_base = pygame.image.load("src/sprites/slime_base.png").convert_alpha()
        parray = pygame.PixelArray(self.img_base)
        parray.replace(settings.WHITE, settings.GREY)
        self.img_over = pygame.image.load("src/sprites/baddies/bandit_over.png")

    def take_turn(self):
        """
        Bandits are dumb, they just attack the nearest player
        """

        match self.turn[self.turn_ptr]:
            case "move":

                if not self.target:
                    closest = None
                    for player in settings.current_scene.players:
                        if player.hp > 0:
                            if not closest:
                                closest = player
                            elif settings.distance(self.pos, player.pos) < settings.distance(self.pos, closest.pos):
                                closest = player
                    self.target = closest
                else:
                    stopped = False
                    if not self.in_melee(self.target):
                        stopped = self.move_towards(self.target.pos)
                    if self.in_melee(self.target) or stopped:
                        self.turn_ptr += 1
            case "action":
                if self.target:
                    if self.in_melee(self.target):
                        self.target.take_damage(self.damage)
                        self.target = None
                self.turn_ptr += 1
            case "done":
                self.turn_ptr = 0
                settings.current_scene.is_turn = False

    def move_towards(self, dest):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = dest[0] - self.pos[0], dest[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        stopped = False
        if self.traveled + dist > self.speed:
            if dist - self.speed > 0:
                dist -= self.speed
            stopped = True
        dx, dy = dx / dist, dy / dist  # Normalize
        # Move along this normalized vector towards the player
        self.pos = (self.pos[0] + dx * settings.combat_speed, self.pos[1] + dy * settings.combat_speed)
        self.traveled += math.hypot(self.pos[0], self.pos[1])
        return stopped

    def in_melee(self, target):
        return settings.distance(self.pos, target.pos) <= 10

    def die(self):
        self.kill()
