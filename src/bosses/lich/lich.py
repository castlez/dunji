import random

from src.bosses.lich.skeleton import Skele
from src.enemies.base import Enemy
from src.settings import Settings as settings
from src.statuses.confused import Confused
from src.statuses.poison import Poison


class Lich(Enemy):
    sprite_img = "bosses/lich/lich.png"
    description = "A nasty and powerful lich"
    cr = 10

    def __init__(self, pos, skele_locs):
        super().__init__(pos=pos,
                         name="Lich",
                         hp=80,
                         damage=4,
                         speed=1,
                         description=self.description,
                         sprite_img=self.sprite_img)
        self.casted_debuffs = False  # cast debuffs at the beginning
        self.color = settings.BLACK
        self.skele_locs = skele_locs
        self.spawn_skele = False

    def take_damage(self, damage):
        before_hp = self.hp
        super().take_damage(damage)
        # check if we passed below half hp
        if before_hp > (self.max_hp / 2) > self.hp:
            # we dropped below half health, ENRAGE
            self.casted_debuffs = False
            settings.log.bad("has become enraged!", self)

    def take_turn(self):
        super().take_turn()
        if not self.casted_debuffs:
            # everyone is poisoned, random player is confused
            for player in settings.players:
                player.statuses.append(Poison(target=player,
                                              duration=3))
            settings.log.bad("inflicts players with poison", self)
            i = random.randint(0, len(settings.players) - 1)
            settings.players[i].statuses.append(Confused(target=settings.players[i],
                                                         duration=3))
            settings.log.bad(f"has become confused!", settings.players[i])
            self.casted_debuffs = True
        if self.spawn_skele:
            # spawn a skele ever other turn up to five
            loc = random.choice(self.skele_locs)
            if len([e for e in settings.current_scene.enemies if type(e) == Skele]) < 5:
                settings.current_scene.enemies.append(Skele(pos=loc))
            self.spawn_skele = False
        else:
            self.spawn_skele = True
        settings.current_scene.is_turn = False
