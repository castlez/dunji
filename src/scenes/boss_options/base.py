import pygame

from src.classes.traits.alignment.chaotic import ChaoticAlignment
from src.classes.traits.alignment.demon import DemonAlignment
from src.classes.traits.alignment.lawful import LawfulAlignment
from src.classes.traits.alignment.neutral import NeutralAlignment
from src.classes.traits.alignment.saint import SaintAlignment
from src.engine import render, mouse
from src.settings import Settings as settings


class BossOption:

    def __init__(self, name, prompt, img, icon_img):
        self.name = name
        self.prompt = prompt
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.topleft = (195, 10)
        self.icon_img = icon_img

        self.done = False  # set early if first voter has resolved the encounter

        self.start_img = pygame.image.load("src/sprites/ui/cbt_start.png")
        self.start_rect = self.start_img.get_rect()
        self.start_rect.topleft = (128.0, 186.8)
        self.done_img = pygame.image.load("src/sprites/ui/done.png")
        self.done_rect = self.done_img.get_rect()
        self.done_rect.topleft = (128.0, 186.8)

        # prompt box
        prompt_y = 16
        self.prompt_img = pygame.image.load("src/sprites/ui/vert2.png")

        # determine prompt box size based on the longest line in the prompt
        prompt_x = 0
        for line in self.prompt:
            size = render.get_text_size(line)[0]
            if size > prompt_x:
                prompt_x = size
        self.prompt_img = pygame.transform.scale(self.prompt_img, (prompt_x, 16*len(self.prompt)))
        self.prect = self.prompt_img.get_rect()
        self.prect.topleft = (settings.WIDTH - prompt_x - 5, prompt_y)

        # final outcome
        # will be one of the choices if the encounter is resolved normally
        # will be something special if it was resolved by the first voter's traits/state
        self.outcome = None

    def get_map_icon(self):
        return pygame.image.load(self.icon_img)

    def resolve(self):
        """
        Each encounter needs to implement this method
        in order to resolve the encounter's effects
        """
        pass

    def start(self):
        """
        start the boss encounter
        :return:
        """
        pass

    def update(self):
        for player in settings.players:
            player.update()
        if settings.current_scene.phase == 0:
            m = (mouse.get_pos()[0], mouse.get_pos()[1])
            # checking if start button was pressed
            if mouse.get_pressed()[0]:
                if self.start_rect.collidepoint(m):
                    settings.current_scene.phase = 1
                    self.start()

    def draw(self, screen):
        # event image
        screen.blit(self.img, self.rect.topleft)
        if settings.current_scene.phase == 0:
            # prompt
            screen.blit(self.prompt_img, self.prect.topleft)
            for i, line in enumerate(self.prompt):
                render.render_text(line, (self.prect.topleft[0], self.prect.topleft[1] + 16*i))
            screen.blit(self.start_img, self.start_rect.topleft)
