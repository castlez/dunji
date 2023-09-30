import pygame.sprite


class Log(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load("src/sprites/ui/vert.png")
        self.img = pygame.transform.scale(self.img, (200, 70))
        self.rect = self.img.get_rect()
        self.rect.topleft = pos
        self.show = False
        self.show_lines = 6  # how many lines to show

        # prepopulate with some lines
        self.lines = []
        self.cur_line = 0
        self.good("Welcome to Dunji!")
        self.good("As the DM, guide your party")
        self.good("5 sessions in a campaign")
        self.good("5 encounters per session")
        self.good("Good luck!")
        self.note("('h' for help, 'l' for log)")

    def set_pos(self, pos):
        self.rect.topleft = pos

    def update(self):
        pass

    def draw_log_box(self, screen):
        if self.show:
            screen.blit(self.img, self.rect)

    def draw(self):
        from src.engine import render
        from src.settings import Settings as settings
        if self.show:
            # write the last 5 lines appended to the log
            cur_x = self.rect.x + 2
            cur_y = self.rect.y + 2
            if self.cur_line - self.show_lines < 0:
                begin = 0
            else:
                begin = self.cur_line - self.show_lines
            lines = self.lines[begin:self.cur_line]
            box_height = self.img.get_height() * settings.SCALEFACTOR
            size = box_height // self.show_lines
            buff = size // 2
            for line in lines:
                text = "> " + line[0]
                render.render_text(text, (cur_x, cur_y), color=line[1], size=size, scaled=True)
                cur_y += buff

    def good(self, text):
        from src.settings import Settings as settings
        self.add_line(text, settings.BGREEN)

    def bad(self, text):
        from src.settings import Settings as settings
        self.add_line(text, settings.RED)

    def info(self, text):
        from src.settings import Settings as settings
        self.add_line(text, settings.WHITE)

    def note (self, text):
        from src.settings import Settings as settings
        self.add_line(text, settings.YELLOW)

    def add_line(self, text, color):
        self.lines.append((text, color))
        self.cur_line += 1
