import pygame


class Item(pygame.sprite.Sprite):

    def __init__(self, name, description, img, value):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.description = description
        self.img = img
        self.rect = self.img.get_rect()
        self.value = value
        self.count = 1

    def use(self, target):
        raise NotImplementedError()
