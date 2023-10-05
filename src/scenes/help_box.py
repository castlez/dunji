

import pygame

from src.engine import render
from src.settings import Settings as settings


class HelpBox(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("src/sprites/ui/vert.png")
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (settings.WIDTH / 2, settings.HEIGHT / 2)
        self.text = [""]

    def update(self):
        match type(settings.current_scene).__name__:
            case "MapScene":
                self.text = ["This is the session plan",
                             "",
                             "Select one of the options for",
                             "    the current encounter.",
                             "",
                             "Dead party members are revived",
                             "    at half health in shops.",
                             "",
                             "Combat encounters are scaled ",
                             "    by encounter level ",
                             "    and current chaos."]
            case "CombatScene":
                self.text = ["This is COMBAT",
                             "",
                             "First, place enemies until",
                             "    the encounter CR is met.",
                             "",
                             "Then press start and watch the",
                             "    combat unfold."]
            case "ShopScene":
                self.text = ["This is the shops",
                             "",
                             "First select a shop to blacklist.",
                             "Players will not visit that shop.",
                             "",
                             "Then press start",
                             "",
                             "Held gems will (usually)",
                             "    be sold for coins.",
                             "",
                             "Players will buy items ",
                             "    according to their own ",
                             "    priorities."]
            case "NCEScene":
                self.text = ["This is a non-combat encounter.",
                             "",
                             "Players will vote on which",
                             "    option to chose based on ",
                             "    their alignment",
                             "",
                             "Chose the vote order, the first",
                             "    vote will count more.",
                             "",
                             "The first voter will try to apply",
                             "    their traits to the situation.",
                             "",
                             "Press start when ready",
                             "    (ctrl+z to re-chose.)"]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        buff = render.get_text_size("test")[1] + 2
        for i, line in enumerate(self.text):
            render.render_text(line, (self.rect.topleft[0], self.rect.topleft[1] + i*buff))
