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
        self.spell_target = coords.get_new_dest_through(pos, spell_target.rect.topleft, settings.WIDTH, settings.HEIGHT)
        dest = spell_target.rect.topleft
        rotation = -1 * math.degrees(math.atan2(dest[1] - self.rect.topleft[1], dest[0] - self.rect.topleft[0]))
        self.img = pygame.transform.rotate(self.img, rotation)

        self.alive = True

    def on_hit(self, target):
        raise NotImplementedError()

    def die(self):
        self.alive = False
        self.kill()

    def check_range(self):
        """
        Check if we are out of range and the spell
        needs to fizzle
        :return:
        """
        if coords.distance(self.start_pos, self.rect.topleft) > self.range:
            return True
        return False

    def update(self):
        """
        move the spell towards its target
        if it hits, call on_hit and return True
        """
        # check spell collision
        for enemy in settings.current_scene.enemies:
            if self.rect.colliderect(enemy.rect):
                self.on_hit(enemy)
                if self.level == 0:
                    self.die()
                    return True
                break

        self.rect.topleft = coords.get_next_pos_towards(self.rect.topleft, self.spell_target, settings.combat_speed)
        if self.check_range():
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
    name = "Fire Bolt"

    def __init__(self, pos, spell_target, level):
        super().__init__(pos=pos,
                         spell_target=spell_target,
                         name="Fire Bolt",
                         level=0,
                         damage=3,
                         healing=0,
                         target_type="enemy",
                         spell_range=self.range,
                         description=self.description,
                         img=self.img)

    def on_hit(self, target):
        # already level 0 so it will only hit one thing
        dmg = random.randint(self.damage-settings.chaos, self.damage + settings.chaos)
        target.take_damage(dmg)
        settings.log.info(f"got hit by fireball for {dmg}!", target)

    def check_range(self):
        """
        Override check range to fly until out of levels
        or off screen
        :return:
        """
        if self.rect.x > settings.WIDTH or self.rect.x < 0 or self.rect.y > settings.HEIGHT or self.rect.y < 0:
            return True
        return False


# First Level
class MagicMissile(Spell):
    range = 150
    img = pygame.image.load("src/sprites/pc/witch_magic_missile.png")
    description = "Magic Darts, can be upcasted for more darts"
    name = "Magic Missile"

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
        # set level so its actually goes up every 2 levels
        self.level = max(1, int(math.floor(level / 2)))

    def on_hit(self, target):
        # do damage + level, then decrease the level until its 0
        if self.level > 0:
            dmg = self.level + self.damage
            target.take_damage(dmg)
            settings.log.info(f"got hit by Magic Missile for {dmg}!", target)
            self.level -= 1

    def check_range(self):
        """
        Override check range to fly until out of levels
        or off screen
        :return:
        """
        if self.rect.x > settings.WIDTH or self.rect.x < 0 or self.rect.y > settings.HEIGHT or self.rect.y < 0:
            return True
        return False

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

