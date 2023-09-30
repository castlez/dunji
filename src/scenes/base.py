import pygame

from src.settings import Settings as settings
from src.engine import render, mouse


class Scene:

    info_box = pygame.image.load("src/sprites/ui/info_box.png")

    info_box_pos = None

    done = False

    log_pos = (200, 230)
    show_log = False

    @staticmethod
    def get_map_icon():
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def draw(self, screen):
        # states shown on every screen
        stat_start = (5, 5)
        stat_step = 10
        stats = [
            f"Party Level: {settings.party_level}",
            f"Chaos: {settings.chaos}",
            f"Help: 'h'",
        ]
        for stat in stats:
            render.render_text(stat, stat_start)
            stat_start = (stat_start[0], stat_start[1] + stat_step)

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
                        if item.count < 0:
                            color = settings.RED
                        else:
                            color = settings.WHITE
                        render.render_text(f"X{item.count}",
                                           (item_start[0] + 20, item_start[1] + item_step*i),
                                           color=color)
                elif player.show_status == "traits":
                    for i, trait in enumerate(player.traits):
                        rect = trait.img.get_rect()
                        rect.topleft = (item_start[0], item_start[1] + item_step*i)
                        screen.blit(trait.img,
                                    rect.topleft)
                        m = mouse.get_pos()
                        if rect.collidepoint(m):
                            render.render_text(trait.name,
                                               (m[0] + 10, m[1] + 10))
                            render.render_text(trait.description,
                                               (m[0] + 10, m[1] + 20))
                elif player.show_status == "statuses":
                    for i, stat in enumerate(player.statuses):
                        rect = stat.img.get_rect()
                        rect.topleft = (item_start[0], item_start[1] + item_step*i)
                        screen.blit(stat.img,
                                    rect.topleft)
                        m = mouse.get_pos()
                        if rect.collidepoint(m):
                            render.render_text(stat.name,
                                               (m[0] + 10, m[1] + 10))
                            render.render_text(stat.description,
                                               (m[0] + 10, m[1] + 20))
                            render.render_text(stat.duration,
                                               (m[0] + 10, m[1] + 30))
