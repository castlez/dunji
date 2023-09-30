import pygame.sprite


class Log(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load("src/sprites/ui/vert.png")
        self.img = pygame.transform.scale(self.img, (200, 70))
        self.rect = self.img.get_rect()
        self.rect.topleft = pos
        self.show = False
        self.show_lines = 5  # how many lines to show
        self.lines = [
            "Welcome to Dunji!",
            "As the DM, guide your part through the dungeon",
            "There are 5 sessions in a campaign",
            "And 5 floors per session",
            "Good luck!",
            "(press 'l' to toggle this log)"
        ]

    def set_pos(self, pos):
        self.rect.topleft = pos

    def update(self):
        pass

    def draw(self, screen):
        from src.engine import render
        if self.show:
            screen.blit(self.img, self.rect)
            # write the last 5 lines appended to the log
            cur_x = self.rect.x + 2
            cur_y = self.rect.y + 2
            lines = self.lines[:self.show_lines]
            line_buffer = 5
            for line in lines:
                render.render_text(line, (cur_x, cur_y))
                cur_y += render.get_text_size(line)[1] + line_buffer
