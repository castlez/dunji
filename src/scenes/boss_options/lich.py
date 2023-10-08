import pygame

from src.bosses.lich.lich import Lich
from src.engine import keys
from src.scenes.boss_options.base import BossOption
from src.settings import Settings as settings
from src.classes.traits.giver import Giver


class LichEvent(BossOption):

    def __init__(self):
        super().__init__(name="Lich",
                         prompt=[
                             "The party enters a musty graveyard. ",
                             "Ancient broken tombstones litter the ground.",
                             "From the other side of the graveyard, ",
                             "a dark figure approaches.",
                             "\"FOOLS! You have interrupted my slumber! ",
                             "MINIONS, DESTROY THEM!\""
                         ],
                         img=pygame.image.load("src/sprites/bosses/lich/lich_scene.png"),
                         icon_img="src/sprites/bosses/lich/lich_icon.png")
        # skeleton spawn locations
        self.skeleton_locs = [
            (240.8, 53.2),
            (280.0, 86.0),
            (349.6, 47.6),
            (271.2, 184.4)
        ]
        self.lich = None
        self.lich_loc = (300, 100)

        # combat stuff
        self.turn_order = []
        self.is_turn = False
        self.current_initiative = 0

    def start(self):
        self.lich = Lich(pos=self.lich_loc, skele_locs=self.skeleton_locs)
        settings.current_scene.enemies = [self.lich]
        self.turn_order = settings.current_scene.enemies + settings.players
        settings.current_scene.is_turn = True
        settings.log.show = True

    def resolve(self):
        pass

    def update(self):
        super().update()
        if settings.current_scene.phase == 1:
            # COMBAT
            new_enemies = []
            for enemy in settings.current_scene.enemies:
                if enemy.alive:
                    new_enemies.append(enemy)
            settings.current_scene.enemies = new_enemies
            if not settings.current_scene.enemies:
                settings.current_scene.phase = 2
                return
            for obj in settings.current_scene.objects:
                obj.update()
            # rebuild turn order excluding dead enemies
            self.turn_order = [e for e in settings.current_scene.enemies if e.alive] + settings.players
            if self.current_initiative > len(self.turn_order) - 1:
                self.current_initiative = 0

            if not settings.current_scene.is_turn:
                if settings.fast_play or keys.get("space", up=True):
                    print(f"{[c.name for c in self.turn_order]}")
                    self.current_initiative += 1
                    if self.current_initiative >= len(self.turn_order):
                        self.current_initiative = 0
                    settings.current_scene.is_turn = True
                    self.turn_order[self.current_initiative].start_turn()
                    self.turn_order[self.current_initiative].take_turn()
            else:
                self.turn_order[self.current_initiative].take_turn()

    def draw(self, screen):
        super().draw(screen)
        for c in self.turn_order:
            c.draw(screen)
