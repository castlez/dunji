import sys

import pygame

from src.classes.witch import Witch
from src.engine import mouse
from src.scenes.combat import CombatScene
from src.scenes.map import MapScene
from src.scenes.title import TitleScene
from src.settings import Settings as settings

pygame.init()


def main():

    # Initial setup
    clock = pygame.time.Clock()
    settings.initialize()

    # Init first scene (TODO update this to actually flow like a game)
    settings.players = [Witch(color=settings.RED), Witch(color=settings.BLUE), Witch(color=settings.GREEN)]
    settings.current_scene = TitleScene()

    # Main Loop
    while True:
        clock.tick(settings.FRAMERATE)

        # check for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # DEBUG

            # detect shift + left click
            # for displaying mouse coordinates (scaled by settings.SCALEFACTOR)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        print(mouse.get_pos()[0], mouse.get_pos()[1])

        # fill screen black
        settings.screen.fill(settings.BLACK)

        # update scene
        settings.current_scene.update()

        # draw scene
        settings.current_scene.draw(settings.screen)

        new_size = (settings.window.get_width(), settings.window.get_height())
        settings.window.blit(pygame.transform.scale(settings.screen, new_size), (0, 0))
        pygame.display.update()


# start game
main()
