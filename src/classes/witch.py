from src.classes.abilities.witch import *


class Witch(Class):

    def __init__(self, color, starting_inven, traits):
        super().__init__(name="witch",
                         hit_die=4,
                         speed=30,
                         sprite_img="pc/witch.png",
                         color=color,
                         starting_inven=starting_inven,
                         traits=traits)

        # spell stuff
        self.cantrip = FireBolt
        self.known_spells: list[type] = [MagicMissile]
        self.spells: list[type] = copy.deepcopy(self.known_spells)
        self.spells_in_flight = []
        self.abilities = [self.cantrip] + self.spells
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
                                    dist_to_enemy = coords.distance(self.rect.topleft, enemy.rect.topleft)
                                    dist_to_closest = coords.distance(self.rect.topleft, closest.rect.topleft)
                                    if not closest:
                                        closest = enemy
                                    elif dist_to_enemy < dist_to_closest:
                                        closest = enemy
                            self.target = closest
                    if self.target:
                        next = self.get_next_position(self.target)  # next position to away from target
                        min_cast_range = self.current_spell.range - self.spell_range_tol
                        dist_to_target = coords.distance(self.rect.topleft, self.target.rect.topleft)
                        if min_cast_range < dist_to_target < self.current_spell.range or \
                                (self.traveled + settings.combat_speed > self.speed and
                                 dist_to_target < self.current_spell.range):
                            # we are in the proper range to cast the spell
                            # or we are in range and cant move anymore
                            self.turn_ptr += 1
                            self.traveled = 0

                            # cast the spell
                            s = self.current_spell(self.rect.topleft, self.target, self.level)
                            self.spells_in_flight.append(s)
                            self.target = None
                        elif min_cast_range > dist_to_target:
                            # we are too close to cast the spell, so move away if we can
                            self.rect.topleft = next
                            self.traveled += settings.combat_speed
                        elif dist_to_target > min_cast_range and self.traveled + settings.combat_speed < self.speed:
                            # we are too far to cast, need to move towards our target
                            self.rect.topleft = coords.get_next_pos_towards(self.rect.topleft, self.target.rect.topleft, settings.combat_speed)
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
        dx, dy = target.rect.topleft[0] - self.rect.topleft[0], target.rect.topleft[1] - self.rect.topleft[1]
        dest = (self.rect.topleft[0] - dx, self.rect.topleft[1] - dy)
        new_pos = coords.get_next_pos_towards(self.rect.topleft, dest, settings.combat_speed)
        if new_pos[0] < 0 or new_pos[0] > settings.WIDTH or \
                new_pos[1] < 0 or new_pos[1] > settings.HEIGHT:
            # if we are going to move off screen, move towards the center instead i guess?
            dest = (settings.WIDTH / 2, settings.HEIGHT / 2)
        return coords.get_next_pos_towards(self.rect.topleft, dest, settings.combat_speed)
