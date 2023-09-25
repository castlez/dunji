"""
Combat Scene

Combat happens in Three phases:
    0. DM places monsters and events
    1. Automatic fight occurs
    2. Rewards/Outcomes
"""
import pygame

from src.enemies.bandit import Bandit
from src.enemies.base import Enemy
from src.settings import Settings as settings
from src.scenes.base import Scene
from src.engine.mouse import Mouse as mouse
from src.engine.keys import Keys as keys


class CombatScene(Scene):
    phase = 0  # 0 is place phase, 1 is fight phase, 2 is outcome
    enemies = None  # filled in the place phase
    players = None  # filled on init
    holding = None  # used for dragging enemies

    # screen locations
    player_screen_start = (12, 230)
    status_screen_start = (200, 230)

    # Player starting positions
    start_pos = [(50, 50), (78, 82), (50, 114)]
    enemy_list_start = status_screen_start
    enemy_list_step = 32

    # Place Phase
    available_enemies = None  # list of enemies to place
    place_img_pos = (195, 10)
    place_range = [[195, 10], [380, 210]]  # [top left, bottom right]
    place_text_pos = (199, 16)
    objective_pos = (7, 154)
    objective_range = [[7, 154], [189, 217]]
    obj_text_pos = (8, 157)
    start_cbt_pos = (11, 190)

    # current turn pointer
    current_initiative = -1  # [self.players, self.enemies]

    # this captures if someone is currently taking a turn
    # set back to false by the player/enemy when they finish their turn
    is_turn = False

    def __init__(self, players):
        # Init combat phase
        # TODO generate this based on player level, progression, and chaos
        # self.objective_cr = 3 + settings.party_level
        self.objective_cr = 3  # TODO set to one for testing
        self.available_enemies: list[type[Enemy]] = [Bandit, Bandit, Bandit]
        self.players = players
        self.enemies = []
        self.turn_order = []
        for player in self.players:
            player.pos = self.start_pos.pop(0)

        # general ui
        self.img = pygame.image.load("src/sprites/ui/combat_ui.png")
        self.img = pygame.transform.scale(self.img, (settings.WIDTH, settings.HEIGHT))

        # placement ui
        self.objective_box = pygame.image.load("src/sprites/ui/cbt_objective_box.png")
        self.place_img = pygame.image.load("src/sprites/ui/cbt_place_ind.png")
        self.start_img = pygame.image.load("src/sprites/ui/cbt_start.png")

        # place the enemy options for this encounter
        self.display_enemy_options = []
        for i, enemy in enumerate(self.available_enemies):
            l1 = pygame.image.load(f"src/sprites/{enemy.sprite_layers[0]}")
            l2 = pygame.image.load(f"src/sprites/{enemy.sprite_layers[1]}")
            self.display_enemy_options.append((l1,
                                               l2,
                                               (self.enemy_list_start[0] + i * self.enemy_list_step, self.enemy_list_start[1]),
                                               i))

    def update_place_phase(self):
        """
        in the placement phase, the DM places enemies and objects
        then presses start to begin the combat encounter
        """
        if self.holding is None:
            if mouse.get_pressed()[0]:
                m = (mouse.get_pos()[0], mouse.get_pos()[1])
                # check if we grabbed an enemy from self.display_enemy_options
                for i, enemy in enumerate(self.display_enemy_options):
                    if enemy[2][0] < m[0] < enemy[2][0] + enemy[0].get_width():
                        if enemy[2][1] + enemy[0].get_height() > m[1] > enemy[2][1]:
                            l1 = pygame.image.load(f"src/sprites/{self.available_enemies[i].sprite_layers[0]}")
                            l2 = pygame.image.load(f"src/sprites/{self.available_enemies[i].sprite_layers[1]}")
                            self.holding = (l1, l2, m, i)
                else:
                    # checking if start button was pressed
                    if self.start_cbt_pos[0] < m[0] < self.start_cbt_pos[0] + self.start_img.get_width():
                        if self.start_cbt_pos[1] + self.start_img.get_height() > m[1] > self.start_cbt_pos[1]:
                            if self.current_cr >= self.objective_cr:
                                # go to the fight phase
                                # self.turn_order = self.players + self.enemies
                                self.turn_order = self.enemies
                                self.phase = 1
                            else:
                                pass  # TODO display error message
            else:
                # TODO fix this so its not machine gun mode
                # TODO go into keys.get and make it so it only returns true once per keypress if once is passed
                if keys.get("ctrl+z", once=True) and self.enemies:
                    n = self.enemies[:-1]
                    self.enemies[-1].die()
                    self.enemies = n

        else:
            # we are holding an enemy
            if not mouse.get_pressed()[0]:  # try to place enemy in hand
                self.try_place_enemy()
                self.holding = None
            else:  # move enemy in hand
                self.holding = (self.holding[0], self.holding[1],
                                (mouse.get_pos()[0] - self.holding[0].get_width() // 2,
                                 mouse.get_pos()[1] - self.holding[0].get_height() // 2),
                                self.holding[3])

    def update_fight_phase(self):
        """
        in the fight phase, the DM watches the fight happen
        """
        if not self.is_turn:
            self.current_initiative += 1
            if self.current_initiative >= len(self.turn_order):
                self.current_initiative = 0
            self.is_turn = True
            self.turn_order[self.current_initiative].take_turn()
        else:
            self.turn_order[self.current_initiative].take_turn()

    def update(self):
        match self.phase:
            case 0:  # place
                self.update_place_phase()
            case 1:  # fight
                self.update_fight_phase()
            case 2:  # outcome
                pass
            case _:
                raise NotImplementedError()

    def draw_place_phase(self, screen):
        # display placement box
        screen.blit(self.place_img, self.place_img_pos)
        settings.render_text(f"Place enemies and objects",
                             self.place_text_pos,
                             color=settings.RED)

        # display objective box
        screen.blit(self.objective_box, self.objective_pos)
        settings.render_text(f"Current CR: {self.current_cr}",
                             self.obj_text_pos,
                             color=settings.WHITE if self.current_cr < self.objective_cr else settings.GREEN)
        settings.render_text(f"Required CR: {self.objective_cr}",
                             (self.obj_text_pos[0], self.obj_text_pos[1] + 10))
        settings.render_text(f"Combat Traits: ",
                             (self.obj_text_pos[0], self.obj_text_pos[1] + 20))
        screen.blit(self.start_img, self.start_cbt_pos)

        # current combatants
        for player in self.players:
            player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)

        # enemy placement options
        for opt in self.display_enemy_options:
            screen.blit(opt[0], opt[2])
            screen.blit(opt[1], opt[2])

        # currently held enemy
        if self.holding:
            screen.blit(self.holding[0], self.holding[2])
            screen.blit(self.holding[1], self.holding[2])

    def draw(self, screen):
        screen.blit(self.img, (0, 0))
        match self.phase:
            case 0:  # place
                self.draw_place_phase(screen)
            case 1:  # fight
                # current combatants
                for player in self.players:
                    player.draw(screen)
                for enemy in self.enemies:
                    enemy.draw(screen)
            case 2:  # outcome
                pass
            case _:
                raise NotImplementedError()

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
        m = mouse.get_pos()
        if self.place_range[0][0] < m[0] < self.place_range[1][0]:
            if self.place_range[0][1] < m[1] < self.place_range[1][1]:
                # add the enemy at the given position
                # ignore the constructor error, types are jank in python
                new_pos = (m[0] - self.holding[0].get_width() // 2, m[1] - self.holding[0].get_height() // 2)
                self.enemies.append(self.available_enemies[self.holding[3]](pos=new_pos))
                self.holding = None

    # fight phase
    def get_current_enemies(self):
        return self.enemies

    def get_current_players(self):
        return self.players