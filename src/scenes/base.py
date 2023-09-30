import pygame

from src.settings import Settings as settings
from src.engine import render


class Scene:

    info_box = pygame.image.load("src/sprites/ui/info_box.png")

    info_box_pos = None

    done = False

    @staticmethod
    def get_map_icon():
        raise NotImplementedError()

    def get_info_box_data(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def draw(self, screen):
        item_start = (self.info_box_pos[0] + 8, self.info_box_pos[1] + 20)
        item_step = 34
        for i, player in enumerate(settings.players):
            player.draw_status(screen)
            if player.show_status:
                screen.blit(self.info_box, self.info_box_pos)
                render.render_text(f"p{i + 1} {player.show_status}",
                                     (self.info_box_pos[0] + 8,
                                      self.info_box_pos[1] + 5))
                if player.show_status == "inven":
                    for i, item in enumerate(player.inven):
                        screen.blit(item.img,
                                    (item_start[0], item_start[1] + item_step*i))
                        render.render_text(f"X{item.count}",
                                             (item_start[0] + 20, item_start[1] + item_step*i))
