import pygame


class Status(pygame.sprite.Sprite):

    def __init__(self, name, description, duration, img, target):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.description = description
        self.duration = duration
        self.img = img
        self.rect = self.img.get_rect()
        self.target = target

    def enact(self):
        """
        Status always enact on the same thing (enemy or player)
        and always at the beginning of
        the things turn
        :return:
        """
        raise NotImplementedError()
