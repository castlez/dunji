from src.enemies.base import Enemy
from src.settings import Settings as settings
from src.engine import coords


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
                    self.target = self.get_target()
                else:
                    stopped = False
                    if not self.in_melee(self.target):
                        stopped = self.move_towards(self.target.rect.topleft)
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
