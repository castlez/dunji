import copy
import math
import random

import pygame

from src.classes.abilities.base import Ability
from src.classes.base import Class
from src.settings import Settings as settings
from src.engine import coords


class Spell(Ability):

    def __init__(self, pos, spell_target, name, level, damage, healing, target_type, spell_range, description, img):
        super().__init__(name=name, description=description, img=img)
        self.rect.topleft = pos
        self.level = level
        self.damage = damage
        self.healing = healing
        self.target_type = target_type
        self.range = spell_range
        self.start_pos = pos
        self.spell_target = spell_target
        dest = self.spell_target.rect.topleft
        rotation = -1 * math.degrees(math.atan2(dest[1] - self.rect.topleft[1], dest[0] - self.rect.topleft[0]))
        self.img = pygame.transform.rotate(self.img, rotation)

        self.alive = True

    def on_hit(self, target):
        raise NotImplementedError()

    def die(self):
        self.alive = False
        self.kill()

    def update(self):
        """
        move the spell towards its target
        if it hits, call on_hit and return True
        """
        # check spell collision
        self.rect.topleft = self.rect.topleft
        if self.rect.colliderect(self.spell_target.rect):
            self.die()
            self.on_hit(self.spell_target)
            return True
        else:
            self.rect.topleft = coords.get_next_pos_towards(self.rect.topleft, self.spell_target.rect.topleft, settings.combat_speed)
            if coords.distance(self.start_pos, self.rect.topleft) > self.range:
                # failsafe, but shouldn't happen since pc only fires if in range
                self.die()
                return True
            return False

    def draw(self, screen):
        if self.alive:
            screen.blit(self.img, self.rect.topleft)

# Cantrips (cant be upcasted)


class FireBolt(Spell):
    range = 110
    img = pygame.image.load("src/sprites/pc/witch_fire_bolt.png")
    description = "Basic fire spell"

    def __init__(self, pos, spell_target, level):
        super().__init__(pos=pos,
                         spell_target=spell_target,
                         name="Fire Bolt",
                         level=0,
                         damage=2,
                         healing=0,
                         target_type="enemy",
                         spell_range=self.range,
                         description="Basic fire spell",
                         img=pygame.image.load("src/sprites/pc/witch_fire_bolt.png"))

    def on_hit(self, target):
        settings.log.info(f"{target.name} got hit by fireball for {self.damage}!")
        target.take_damage(self.damage)


# First Level
class MagicMissile(Spell):
    range = 150
    img = pygame.image.load("src/sprites/pc/witch_magic_missile.png")
    description = "Magic Darts, can be upcasted for more darts"

    def __init__(self, pos, spell_target, level):
        super().__init__(pos=pos,
                         spell_target=spell_target,
                         name="Magic Missle",
                         level=level,
                         damage=4,
                         healing=0,
                         target_type="enemy",
                         spell_range=self.range,
                         description=self.description,
                         img=self.img)

    def on_hit(self, target):
        total = 0
        for _ in range(self.level):
            total += self.damage
            target.take_damage(self.damage)
        settings.log.info(f"{target.name} got hit by Magic Missile for {total}!")

    def draw(self, screen):
        if self.alive:
            offset = 20
            for i in range(self.level):
                screen.blit(self.img, (self.rect.topleft[0] + offset*i, self.rect.topleft[1]))


class Spellbook:

    @classmethod
    def get_new_spell(cls, level):
        """
        return a spell to add to the witches spell options
        if there is not a special spell for that level, return magic missile
        """
        match level:
            case _:
                return MagicMissile

