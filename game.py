import sys

import pygame

import src.classes.traits.giver
from src.classes.witch import Witch
from src.engine import mouse, keys, render
from src.items.coins import Coins
from src.items.gem import Gem
from src.items.hp_pot import HPPot
from src.log import Log
from src.scenes.combat import CombatScene
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

    # Main Loop
    while True:
        clock.tick(settings.FRAMERATE)

        # back to map
        if settings.current_scene.done:
            settings.current_scene = MapScene()
            settings.current_floor += 1

        # check for exit
        for event in pygame.event.get():
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
            if event.type == pygame.KEYDOWN:
                settings.log.show = not settings.log.show

        # fill screen black
        settings.screen.fill(settings.BLACK)

        # update scene
        settings.current_scene.update()

        # draw scene
        settings.current_scene.draw(settings.screen)

        # draw log
        if settings.log.show:
            settings.log.draw(settings.screen)

        new_size = (settings.window.get_width(), settings.window.get_height())
        settings.window.blit(pygame.transform.scale(settings.screen, new_size), (0, 0))
        pygame.display.update()


# start game
main()
