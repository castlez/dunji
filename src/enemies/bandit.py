import math

import pygame.image

from src.enemies.base import Enemy
from src.settings import Settings as settings
from src.engine.coords import Coords as coords


class Bandit(Enemy):
    # used for enemy placement
    sprite_layers = ["slime_base.png", "baddies/bandit_over.png"]
    cr = 1

    def __init__(self, pos):
        super().__init__(pos=pos,
                         name="Bandit",
                         hp=10,
                         damage=2,
                         speed=60,
                         description="A bandit. He's not very nice.",
                         sprite_layers=self.sprite_layers)

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
                            elif coords.distance(self.rect.center, player.rect.center) < coords.distance(self.rect.center, closest.rect.center):
                                closest = player
                    self.target = closest
                else:
                    stopped = False
                    if not self.in_melee(self.target):
                        stopped = self.move_towards(self.target.rect.center)
                    if self.in_melee(self.target) or stopped:
                        self.turn_ptr += 1
                        self.traveled = 0
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
        dx, dy = dest[0] - self.rect.center[0], dest[1] - self.rect.center[1]
        dist = math.hypot(dx, dy)
        stopped = False
        if self.traveled + settings.combat_speed > self.speed:
            if dist - self.speed > 0:
                stopped = True
        dx, dy = dx / dist, dy / dist  # Normalize
        # Move along this normalized vector towards the player
        pos = (self.rect.center[0] + dx * settings.combat_speed, self.rect.center[1] + dy * settings.combat_speed)
        self.move(pos)
        self.traveled += settings.combat_speed
        return stopped

    def in_melee(self, target):
        return coords.distance(self.rect.center, target.rect.center) <= 10
