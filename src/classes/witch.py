import copy
import math
import random

import pygame

from src.classes.base import Class
from src.settings import Settings as settings
from src.engine import coords


# Spells

class Spell(pygame.sprite.Sprite):

    def __init__(self, pos, spell_target, name, level, damage, healing, target_type, spell_range, description, img):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.level = level
        self.damage = damage
        self.healing = healing
        self.target_type = target_type
        self.range = spell_range
        self.description = description
        self.start_pos = pos
        self.spell_target = spell_target
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = pos
        dest = self.spell_target.rect.center
        rotation = -1 * math.degrees(math.atan2(dest[1] - self.rect.center[1], dest[0] - self.rect.center[0]))
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
        self.rect.center = self.rect.center
        if self.rect.colliderect(self.spell_target.rect):
            self.die()
            self.on_hit(self.spell_target)
            return True
        else:
            self.rect.center = coords.get_next_pos_towards(self.rect.center, self.spell_target.rect.center, settings.combat_speed)
            if coords.distance(self.start_pos, self.rect.center) > self.range:
                # failsafe, but shouldn't happen since pc only fires if in range
                self.die()
                return True
            return False

    def draw(self, screen):
        if self.alive:
            screen.blit(self.img, self.rect.center)

# Cantrips (cant be upcasted)


class FireBolt(Spell):
    range = 110

    def __init__(self, pos, spell_target, level):
        super().__init__(pos=pos,
                         spell_target=spell_target,
                         name="Fire Bolt",
                         level=0,
                         damage=2,
                         healing=0,
                         target_type="enemy",
                         spell_range=self.range,
                         description="A basic bolt attack for the witch.",
                         img=pygame.image.load("src/sprites/pc/witch_fire_bolt.png"))

    def on_hit(self, target):
        target.take_damage(self.damage)


# First Level
class MagicMissile(Spell):
    range = 30

    def __init__(self, pos, spell_target, level):
        super().__init__(pos=pos,
                         spell_target=spell_target,
                         name="Magic Missle",
                         level=level,
                         damage=4,
                         healing=0,
                         target_type="enemy",
                         spell_range=self.range,
                         description="A shiny dart flies from the witch's staff, striking the enemy for 4 damage. " \
                                     "Upcasting increases the number of darts",
                         img=pygame.image.load("src/sprites/pc/witch_magic_missile.png"))

    def on_hit(self, target):
        for _ in range(self.level):
            target.take_damage(self.damage)


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


class Witch(Class):

    def __init__(self, color, starting_inven):
        super().__init__(name="witch",
                         hit_die=4,
                         speed=30,
                         sprite_img="pc/witch.png",
                         color=color,
                         starting_inven=starting_inven)

        # spell stuff
        self.cantrip = FireBolt
        self.known_spells: list[type] = []
        self.spells: list[type] = copy.deepcopy(self.known_spells)
        self.spells_in_flight = []
        self.slots = 0
        self.current_spell = None
        self.spell_range_tol = settings.combat_speed  # close enough to max range to cast

    def draw(self, screen):
        super().draw(screen)
        if self.alive:
            for s in self.spells_in_flight:
                s.draw(screen)

    def level_up(self):
        super().level_up()
        if self.level % 2 == 0:
            self.slots += 1
            self.known_spells.append(Spellbook.get_new_spell(self.level))

    def take_turn(self):
        """
        Witch's strategy is to move to max range away from the closes enemy
        and fire their strongest spell at them

        max range is either the range of the spell or the players speed
        """
        if self.alive:
            match self.turn[self.turn_ptr]:
                case "move":
                    if not self.target:
                        # pick a spell to cast if we have one
                        # otherwise cast our cantrip
                        if self.spells:
                            self.current_spell = self.spells.pop(random.randint(0, len(self.spells) - 1))
                        else:
                            self.current_spell = self.cantrip

                        # find the closest enemy
                        if settings.current_scene.enemies:
                            closest = settings.current_scene.enemies[0]
                            for enemy in settings.current_scene.enemies:
                                if enemy.alive:
                                    dist_to_enemy = coords.distance(self.rect.center, enemy.rect.center)
                                    dist_to_closest = coords.distance(self.rect.center, closest.rect.center)
                                    if not closest:
                                        closest = enemy
                                    elif dist_to_enemy < dist_to_closest:
                                        closest = enemy
                            self.target = closest
                    if self.target:
                        next = self.get_next_position(self.target)  # next position to away from target
                        min_cast_range = self.current_spell.range - self.spell_range_tol
                        dist_to_target = coords.distance(self.rect.center, self.target.rect.center)
                        if min_cast_range < dist_to_target < self.current_spell.range or \
                                (self.traveled + settings.combat_speed > self.speed and
                                 dist_to_target < self.current_spell.range):
                            # we are in the proper range to cast the spell
                            # or we are in range and cant move anymore
                            self.turn_ptr += 1
                            self.traveled = 0

                            # cast the spell
                            s = self.current_spell(self.rect.center, self.target, self.level)
                            self.spells_in_flight.append(s)
                            self.target = None
                        elif min_cast_range > dist_to_target:
                            # we are too close to cast the spell, so move away if we can
                            self.rect.center = next
                            self.traveled += settings.combat_speed
                        elif dist_to_target > min_cast_range and self.traveled + settings.combat_speed < self.speed:
                            # we are too far to cast, need to move towards our target
                            self.rect.center = coords.get_next_pos_towards(self.rect.center, self.target.rect.center, settings.combat_speed)
                        else:
                            # we are too far to cast and cant move anymore
                            self.turn_ptr += 1
                            self.traveled = 0
                            self.current_spell = None
                            self.target = None
                case "action":
                    for s in self.spells_in_flight:
                        if s.update():
                            s.alive = False
                    new_list = []
                    for a in self.spells_in_flight:
                        if a.alive:
                            new_list.append(a)
                    self.spells_in_flight = new_list
                    if not self.spells_in_flight:
                        self.turn_ptr += 1
                case "done":
                    self.turn_ptr = 0
                    settings.current_scene.is_turn = False

        else:
            settings.current_scene.is_turn = False

    def get_next_position(self, target):
        # get destination away from target
        dx, dy = target.rect.center[0] - self.rect.center[0], target.rect.center[1] - self.rect.center[1]
        dest = (self.rect.center[0] - dx, self.rect.center[1] - dy)
        new_pos = coords.get_next_pos_towards(self.rect.center, dest, settings.combat_speed)
        if new_pos[0] < 0 or new_pos[0] > settings.WIDTH or \
                new_pos[1] < 0 or new_pos[1] > settings.HEIGHT:
            # if we are going to move off screen, move towards the center instead i guess?
            dest = (settings.WIDTH / 2, settings.HEIGHT / 2)
        return coords.get_next_pos_towards(self.rect.center, dest, settings.combat_speed)
