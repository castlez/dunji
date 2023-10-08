import random

from src.bosses.lich.skeleton import Skele
from src.enemies.base import Enemy
from src.settings import Settings as settings
from src.statuses.confused import Confused
from src.statuses.poison import Poison


class Lich(Enemy):

    def __init__(self, pos, skele_locs):
        super().__init__(pos=pos,
                         name="Lich",
                         hp=20,
                         damage=4,
                         speed=1,
                         description="A nasty and powerful lich",
                         sprite_img="bosses/lich/lich.png")
        self.casted_debuffs = False  # cast debuffs at the beginning
        self.color = settings.BLACK
        self.skele_locs = skele_locs
        self.spawn_skele = False

    def take_turn(self):
        super().take_turn()
        if not self.casted_debuffs:
            # everyone is poisoned, random player is confused
            for player in settings.players:
                player.statuses.append(Poison(target=player,
                                              duration=3))
            settings.log.bad("inflicts players with poison", self)
            # i = random.randint(0, len(settings.players) - 1)
            # conf_player = settings.players[i]
            # conf_player.statuses.append(Confused(target=conf_player,
            #                                      duration=3))
            # settings.log.bad(f"has become confused!", conf_player)
            self.casted_debuffs = True
        if self.spawn_skele:
            # spawn a skele ever other turn
            loc = random.choice(self.skele_locs)
            settings.current_scene.enemies.append(Skele(pos=loc))
        else:
            self.spawn_skele = True
        settings.current_scene.is_turn = False
