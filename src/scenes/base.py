import pygame

from src.settings import Settings as settings


class Scene:

    info_box = pygame.image.load("src/sprites/ui/info_box.png")

    info_box_pos = None

    @staticmethod
    def get_map_icon():
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def get_info_box_data(self):
        raise NotImplementedError()

    def draw(self, screen):
        for i, player in enumerate(settings.players):
            player.draw_status(screen)
            if player.show_status:
                screen.blit(self.info_box, self.info_box_pos)
                settings.render_text(f"p{i + 1} {player.show_status}",
                                     (self.info_box_pos[0] + 5,
                                      self.info_box_pos[1] + 5))
