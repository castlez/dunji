import pygame

class Ability(pygame.sprite.Sprite):

    def __init__(self, name, description, img):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.description = description
        self.img = img
        self.rect = self.img.get_rect()