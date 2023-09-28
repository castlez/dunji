import pygame
from src.engine import mouse
from src.settings import Settings as settings


class Shop(pygame.sprite.Sprite):

    def __init__(self, wares, img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.wares = wares
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = pos
        self.show_wares = False

    def update(self):
        """
        Check if mouse is hover over the shop
        :return:
        """
        if mouse.get_pressed()[0]:
            if self.rect.collidepoint(mouse.get_pos()):
                for other_shop in settings.current_scene.shops:
                    if other_shop != self:
                        other_shop.show_wares = False
                self.show_wares = True
                return

    def draw(self, screen):
        screen.blit(self.img, self.rect)

