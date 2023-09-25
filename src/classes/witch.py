import copy
import random

import pygame

from src.classes.base import Class
from src.settings import Settings as settings

# Spells

class Spell(pygame.sprite.Sprite):

    def __init__(self, pos, angle, name, level, damage, healing, target, description):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.level = level
        self.damage = damage
        self.healing = healing
        self.target = target
        self.description = description

    def cast(self, target):
        raise NotImplementedError()


# Cantrips (cant be upcasted)


class FireBolt(Spell):
    def __init__(self, pos, angle):
        super().__init__(pos=pos,
                         angle=angle,
                         name="Fire Bolt",
                         level=0,
                         damage=2,
                         healing=0,
                         target="enemy",
                         description="A basic bolt attack for the witch.")

    def cast(self, target):
        target.take_damage(self.damage)


# First Level
class MagicMissile(Spell):
    def __init__(self, pos, angle, level):
        super().__init__(pos=pos,
                         angle=angle,
                         name="Magic Missle",
                         level=level,
                         damage=4,
                         healing=0,
                         target="enemy",
                         description="A shiny dart flies from the witch's staff, striking the enemy for 4 damage. " \
                                     "Upcasting increases the number of darts")

    def cast(self, target):
        for _ in range(self.level):
            target.take_damage(self.damage)


class Spellbook:

    @classmethod
    def get_spell(cls, level):
        """
        return a spell to add to the witches spell options
        if there is not a special spell for that level, return magic missile
        """
        match level:
            case _:
                return MagicMissile


class Witch(Class):

    def __init__(self, color):
        super().__init__(name="witch", hit_die=4, speed=30)
        self.known_spells: list[type] = [FireBolt]
        self.spells: list[type] = copy.deepcopy(self.known_spells)
        self.slots = 0
        self.img_base = pygame.image.load("src/sprites/slime_base.png").convert_alpha()
        parray = pygame.PixelArray(self.img_base)
        parray.replace(settings.WHITE, color)
        self.img_over = pygame.image.load("src/sprites/pc/witch_over.png")

        self.pos = (0, 0)

        # TODO roll traits
        self.traits = ["todo"]

    def draw(self, screen):
        if self.alive:
            screen.blit(self.img_base, self.pos)
            screen.blit(self.img_over, self.pos)
        else:
            screen.blit(self.dead_img, self.pos)

    def level_up(self):
        super().level_up()
        if self.level % 2 == 0:
            self.slots += 1
            self.known_spells.append(Spellbook.get_spell(self.level))

    def take_turn(self):
        """
        Witch's strategy is to move to max range away from the closes enemy
        and fire their strongest spell at them
        """
        if self.alive:
            pass
        else:
            settings.current_scene.is_turn = False