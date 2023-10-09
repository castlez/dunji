"""
Combat Scene

Combat happens in Three phases:
    0. DM places monsters and events
    1. Automatic fight occurs
    2. Rewards/Outcomes
"""
import random

import pygame

from src.enemies.bandit import Bandit
from src.enemies.base import Enemy
from src.enemies.kobold import Kobold
from src.settings import Settings as settings
from src.scenes.base import Scene
from src.engine import mouse
from src.engine import keys
from src.engine import render


class CombatScene(Scene):
    phase = 0  # 0 is place phase, 1 is fight phase, 2 is outcome
    enemies = None  # filled in the place phase
    players = None  # filled on init
    holding = None  # used for dragging enemies
    amount = 0  # used for dragging enemies

    # screen locations
    player_screen_start = (12, 230)
    status_screen_start = (200, 230)
    status_y = 225
    p1_display_pos = (22, status_y)
    p2_display_pos = (82, status_y)
    p3_display_pos = (142, status_y)
    info_box_pos = (20, 20)

    # Player starting positions
    start_pos = [(50, 50), (78, 82), (50, 114)]
    enemy_list_start = status_screen_start
    enemy_list_step = 32

    # Place Phase
    available_enemies = None  # list of enemies to place
    place_img_pos = (195, 10)
    place_range = [[190, 10], [380, 210]]  # [top left, bottom right] (190 X 200)
    place_text_pos = (199, 16)
    objective_pos = (7, 154)
    objective_range = [[7, 154], [189, 217]]
    obj_text_pos = (8, 157)
    start_cbt_pos = (11, 190)

    # current turn pointer
    current_initiative = -1  # [settings.players, self.enemies]

    # this captures if someone is currently taking a turn
    # set back to false by the player/enemy when they finish their turn
    is_turn = False

    def __init__(self):
        super().__init__()
        # Init combat phase
        self.objective_cr = self.get_challenge_rating(floor=settings.current_floor)
        self.available_enemies: list[type[Enemy]] = [Bandit, Kobold, Bandit]
        self.enemies = []
        self.turn_order = []
        sp = self.start_pos.copy()
        for player in settings.players:
            player.rect.topleft = sp.pop(0)

        # not player, not enemy objects in combat
        # stuff like exploding barrels and shurikens
        self.objects = []

        # general ui
        self.img = pygame.image.load("src/sprites/ui/gen_ui.png")
        self.img = pygame.transform.scale(self.img, (settings.WIDTH, settings.HEIGHT))
        settings.players[0].status_location = self.p1_display_pos
        settings.players[1].status_location = self.p2_display_pos
        settings.players[2].status_location = self.p3_display_pos

        # placement ui
        self.objective_box = pygame.image.load("src/sprites/ui/cbt_objective_box.png")
        self.place_img = pygame.image.load("src/sprites/ui/cbt_place_ind.png")
        self.start_img = pygame.image.load("src/sprites/ui/cbt_start.png")

        # place the enemy options for this encounter
        self.display_enemy_options = []
        for i, enemy in enumerate(self.available_enemies):
            self.display_enemy_options.append((pygame.image.load(f"src/sprites/{enemy.sprite_img}"),
                                               (self.enemy_list_start[0] + i * self.enemy_list_step,
                                                self.enemy_list_start[1]),
                                               i))

        # log
        settings.log.set_pos((self.enemy_list_start[0] - 5,
                              self.enemy_list_start[1] - 5))

    @staticmethod
    def get_map_icon():
        return pygame.image.load("src/sprites/nav/combat_encounter_icon.png")

    @staticmethod
    def get_description(floor):
        ecr = f"{CombatScene.get_min_cr(settings.get_floor_mod(floor))} - {CombatScene.get_max_cr(settings.get_floor_mod(floor))}"
        return ["A combat encounter",
                f"Expected CR: {ecr}"]

    @staticmethod
    def get_min_cr(floor):
        return settings.base_cr + settings.get_floor_mod(floor) * 3

    @staticmethod
    def get_max_cr(floor):
        return settings.base_cr + (settings.chaos + settings.get_floor_mod(floor) * 3)

    @staticmethod
    def get_challenge_rating(floor):
        return random.randint(CombatScene.get_min_cr(floor), CombatScene.get_max_cr(floor))

    def update_place_phase(self):
        """
        in the placement phase, the DM places enemies and objects
        then presses start to begin the combat encounter
        """
        if self.holding is None:
            if mouse.get_held()[0]:
                m = (mouse.get_pos()[0], mouse.get_pos()[1])
                # check if we grabbed an enemy from self.display_enemy_options
                for i, enemy in enumerate(self.display_enemy_options):
                    if enemy[1][0] < m[0] < enemy[1][0] + enemy[0].get_width():
                        if enemy[1][1] + enemy[0].get_height() > m[1] > enemy[1][1]:
                            self.holding = (enemy[0],
                                            (mouse.get_pos()[0] - enemy[0].get_width() // 2,
                                             mouse.get_pos()[1] - enemy[0].get_height() // 2),
                                            i)
                            if keys.get_number_key():
                                self.amount = keys.get_number_key()
                                print(f"placing {self.amount}")
                else:
                    # checking if start button was pressed
                    if self.start_cbt_pos[0] < m[0] < self.start_cbt_pos[0] + self.start_img.get_width():
                        if self.start_cbt_pos[1] + self.start_img.get_height() > m[1] > self.start_cbt_pos[1]:
                            if self.current_cr >= self.objective_cr:
                                # go to the fight phase
                                self.turn_order = settings.players + self.enemies
                                self.phase = 1
                                settings.log.show = True
                            else:
                                pass  # TODO display error message
            else:
                if keys.get("ctrl+z", up=True) and self.enemies:
                    # undo last enemy placement
                    n = self.enemies[:-1]
                    self.enemies[-1].die()
                    self.enemies = n

        else:
            # we are holding an enemy
            placeable_enemies = self.try_place_enemy()
            if placeable_enemies:
                if not mouse.get_held()[0]:
                    self.holding = None
                    self.enemies += placeable_enemies
                else:
                    img = self.display_enemy_options[self.holding[2]][0].copy()
                    img.fill(settings.GREEN, special_flags=pygame.BLEND_ADD)
                    self.holding = (img,
                                    (mouse.get_pos()[0] - self.holding[0].get_width() // 2,
                                     mouse.get_pos()[1] - self.holding[0].get_height() // 2),
                                    self.holding[2])
            else:  # move enemy in hand
                img = self.display_enemy_options[self.holding[2]][0].copy()
                img.fill(settings.RED, special_flags=pygame.BLEND_ADD)
                self.holding = (img,
                                (mouse.get_pos()[0] - self.holding[0].get_width() // 2,
                                 mouse.get_pos()[1] - self.holding[0].get_height() // 2),
                                self.holding[2])

    def update_fight_phase(self):
        """
        in the fight phase, the DM watches the fight happen
        """
        if not self.enemies:
            self.phase += 1
            return

        # this breaks shit if it goes to high
        # this is because its technically not how fast stuff plays
        # its actually how far things can move in a frame
        # which means distance checks will get fucked up
        if keys.get("up"):
            settings.combat_speed += 1
        if keys.get("down"):
            settings.combat_speed -= 1

        for obj in self.objects:
            obj.update()

        # rebuild turn order excluding dead enemies
        self.turn_order = settings.players + [e for e in self.enemies if e.alive]

        if not self.is_turn:
            if settings.fast_play or keys.get("space", up=True):
                self.current_initiative += 1
                if self.current_initiative >= len(self.turn_order):
                    self.current_initiative = 0
                self.is_turn = True
                self.turn_order[self.current_initiative].start_turn()
                self.turn_order[self.current_initiative].take_turn()
        else:
            self.turn_order[self.current_initiative].take_turn()

    def update(self):
        for player in settings.players:
            player.update()
        match self.phase:
            case 0:  # place
                self.update_place_phase()
            case 1:  # fight
                # reap dead baddies
                new_enemies = []
                for enemy in self.enemies:
                    if enemy.alive:
                        new_enemies.append(enemy)
                self.enemies = new_enemies
                self.update_fight_phase()
            case 2:  # outcome
                # TODO outcome screen
                for player in settings.players:
                    player.level_up()
                settings.party_level += 1
                self.done = True
            case _:
                raise NotImplementedError()

    def draw_place_phase(self, screen):
        # display placement box
        screen.blit(self.place_img, self.place_img_pos)
        render.render_text(f"Place enemies and objects",
                           self.place_text_pos,
                           color=settings.RED)
        render.render_text(f"Hold numbers to add duplicates",
                           (self.place_text_pos[0], self.place_text_pos[1] + 10),
                           color=settings.RED)

        # display objective box
        screen.blit(self.objective_box, self.objective_pos)
        render.render_text(f"Current CR: {self.current_cr}",
                           self.obj_text_pos,
                           color=settings.WHITE if self.current_cr < self.objective_cr else settings.GREEN)
        render.render_text(f"Required CR: {self.objective_cr}",
                           (self.obj_text_pos[0], self.obj_text_pos[1] + 10))
        render.render_text(f"Combat Traits: ",
                           (self.obj_text_pos[0], self.obj_text_pos[1] + 20))
        screen.blit(self.start_img, self.start_cbt_pos)

        # current combatants
        for player in settings.players:
            player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)

        # enemy placement options
        for opt in self.display_enemy_options:
            screen.blit(opt[0], opt[1])

            # if hovering the enemy, render text of its description
            if opt[1][0] < mouse.get_pos()[0] < opt[1][0] + opt[0].get_width():
                if opt[1][1] + opt[0].get_height() > mouse.get_pos()[1] > opt[1][1]:
                    render.render_text(self.available_enemies[opt[2]].__name__,
                                        (mouse.get_pos()[0], mouse.get_pos()[1] - 30))
                    render.render_text(self.available_enemies[opt[2]].description,
                                       (mouse.get_pos()[0], mouse.get_pos()[1] - 20))
                    render.render_text(f"CR: {self.available_enemies[opt[2]].cr}",
                                       (mouse.get_pos()[0], mouse.get_pos()[1] - 10))

        # currently held enemy
        if self.holding:
            screen.blit(self.holding[0], self.holding[1])
            if self.amount:
                num = self.amount - 1  # remove the one you already drew
                cur_x = self.holding[1][0]
                step = 32
                offset = 0
                for i in range(num):
                    offset += step
                    if i == 2:
                        cur_x = self.holding[1][0] + step
                        offset = 0
                    elif i == 5:
                        cur_x = self.holding[1][0] + step * 2
                        offset = 0
                    cur_y = self.holding[1][1] + offset
                    screen.blit(self.holding[0], (cur_x, cur_y))

    def draw(self, screen):
        screen.blit(self.img, (0, 0))
        match self.phase:
            case 0:  # place
                self.draw_place_phase(screen)
            case 1:  # fight
                # render key hints
                if settings.fast_play:
                    render.render_text("Press F to toggle off fast play",
                                       (settings.WIDTH - 100, 10),
                                       color=settings.RED)
                else:
                    render.render_text("Press F to toggle on fast play",
                                       (settings.WIDTH - 100, 10),
                                       color=settings.GREEN)
                    render.render_text("Press SPACE to go to next turn",
                                       (settings.WIDTH - 100, 20),
                                       color=settings.GREEN)
                # current combatants
                for player in settings.players:
                    player.draw(screen)
                for enemy in self.enemies:
                    enemy.draw(screen)
            case 2:  # outcome
                pass
            case _:
                raise NotImplementedError()
        for obj in self.objects:
            obj.draw(screen)
        super().draw(screen)

    # place phase
    def get_enemy_options(self):
        pass

    @property
    def current_cr(self):
        return sum([e.cr for e in self.enemies]) if self.enemies else 0

    def try_place_enemy(self):
        """
        :param enemy: tuple (l1, l2, pos, index_in_available_enemies)
        :return:
        """
        loc = [self.holding[1][0], self.holding[1][1]]
        new_enemies = []
        offset = 0
        step = 32
        num = self.amount if self.amount else 1
        for i in range(num):
            if self.place_range[0][0] < loc[0] < self.place_range[1][0]:
                if self.place_range[0][1] < loc[1] < self.place_range[1][1]:
                    # add the enemy at the given position
                    new_pos = (loc[0], loc[1])
                    new_enemies.append(self.available_enemies[self.holding[2]](pos=new_pos))
                    offset += step
                    if i == 2:
                        loc[0] = self.holding[1][0] + step
                        offset = 0
                    elif i == 5:
                        loc[0] = self.holding[1][0] + step * 2
                        offset = 0
                    loc[1] = self.holding[1][1] + offset
                else:
                    # OVER THE LINE, MARK IT ZERO
                    new_enemies = None
                    break
        return new_enemies

    # fight phase
    def get_current_enemies(self):
        return self.enemies

    def get_current_players(self):
        return settings.players
