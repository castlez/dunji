import pygame


class Trait(pygame.sprite.Sprite):
    # TODO every trait needs to implement an action method
    def __init__(self, name, description, img):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.description = description
        self.img = img
        self.rect = self.img.get_rect()

    def update(self):
        pass  # todo check if mouse over

    def draw(self, screen):
        screen.blit(self.img, self.rect)
