from src.enemies.base import Enemy
from src.settings import Settings as settings
from src.engine.coords import Coords as coords


class Kobold(Enemy):
    # used for enemy placement
    sprite_img = "baddies/kobold.png"
    cr = 1

    def __init__(self, pos):
        super().__init__(pos=pos,
                         name="Kobold",
                         hp=1,
                         damage=1,
                         speed=60,
                         description="A kobold. Little nasty rat",
                         sprite_img=self.sprite_img)

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
