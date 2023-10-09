import sys
from threading import Lock

import pygame

import src.classes.traits.giver
from src.classes.witch import Witch
from src.engine import mouse, keys, render
from src.items.coins import Coins
from src.items.gem import Gem
from src.items.hp_pot import HPPot
from src.log import Log
from src.scenes.combat import CombatScene
from src.scenes.help_box import HelpBox
from src.scenes.map import MapScene
from src.scenes.party_select import PartySelectScene
from src.scenes.shops import ShopScene
from src.scenes.title import TitleScene
from src.settings import Settings as settings

pygame.init()


def main():

    # Initial setup
    clock = pygame.time.Clock()
    settings.initialize()
    settings.log = Log((0, 0))
    settings.log.startup_log()
    help = HelpBox()
    show_help = False

    # Init first scene (TODO update this to actually flow like a game)
    # TODO implement character creation
    # from src.classes.traits.clepto import Clepto
    # from src.classes.traits.sweet_tooth import SweetTooth
    # from src.classes.traits.giver import Giver
    # from src.classes.traits.hoarder import Hoarder
    # from src.classes.traits.peace_keeper import PeaceKeeper
    # from src.classes.traits.sneaky import Sneaky
    # settings.players = [
    #     Witch(color=settings.RED,
    #           starting_inven=[Coins(), Gem()],
    #           traits=[PeaceKeeper(), Sneaky()]),
    #     Witch(color=settings.BLUE,
    #           starting_inven=[Coins(), HPPot()],
    #           traits=[Clepto()]),
    #     Witch(color=settings.GREEN,
    #           starting_inven=[Coins(), Gem()],
    #           traits=[Clepto()])
    # ]
    settings.current_scene = TitleScene()
    settings.current_floor = 4  # TODO debug bosses
    cheat = True
    # Main Loop
    while True:
        clock.tick(settings.FRAMERATE)

        if cheat and type(settings.current_scene) == MapScene:
            for player in settings.players:
                player.level_up()
                player.level_up()
                player.level_up()
                player.rest()
            cheat = False

        # back to map
        if settings.current_scene.done:
            if settings.current_floor == 4:
                # go to the next session
                settings.session += 1
                settings.current_floor = 0
                settings.base_cr += 1
                settings.map = []
                settings.current_scene = MapScene()
            else:
                settings.current_scene = MapScene()
                settings.current_floor += 1

        # check for exit
        settings.events = pygame.event.get()
        for event in settings.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # detect shift + left click
            # for displaying mouse coordinates (scaled by settings.SCALEFACTOR)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        print(mouse.get_pos()[0], mouse.get_pos()[1])
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        settings.chaos += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                settings.log.show = not settings.log.show
            if event.type == pygame.MOUSEWHEEL:
                if settings.log.show:
                    settings.log.scroll(event.y * -1)  # my preferred scroll direction
            if keys.get("f"):
                settings.fast_play = not settings.fast_play
            if keys.get("h"):
                show_help = not show_help
            if keys.get("p"):
                # level up all players
                for player in settings.players:
                    player.level_up()
                settings.party_level += 1

        # fill screen black
        settings.screen.fill(settings.BLACK)

        # update scene
        settings.current_scene.update()
        help.update()

        # draw scene
        settings.current_scene.draw(settings.screen)

        # draw log box before scale
        if settings.log.show:
            settings.log.draw_log_box(settings.screen)

        # draw help box
        if show_help:
            help.draw(settings.screen)

        new_size = (settings.window.get_width(), settings.window.get_height())
        settings.window.blit(pygame.transform.scale(settings.screen, new_size), (0, 0))

        # draw log text after scale
        if settings.log.show:
            settings.log.draw()

        pygame.display.update()


# start game
main()
