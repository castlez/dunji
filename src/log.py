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
                if "|" in line[0]:
                    # player line needs fancy coloring
                    # "Witch|255,255,255|has stolen your gold!"
                    parts = line[0].split("|")
                    pc = parts[0]
                    cparts = parts[1].split(",")
                    color = ( int(cparts[0]), int(cparts[1]), int(cparts[2]))
                    msg = parts[2]
                    render.render_text(pc, (cur_x, cur_y), color=color, size=size, scaled=True)
                    render.render_text(msg, (cur_x + render.get_text_size(pc, size=size, scaled=True)[1], cur_y),
                                       color=line[1], size=size, scaled=True)
                else:
                    text = "> " + line[0]
                    render.render_text(text, (cur_x, cur_y), color=line[1], size=size, scaled=True)
                cur_y += buff

    def good(self, text):
        from src.settings import Settings as settings
        self.add_line(text, settings.BGREEN)

    def bad(self, text):
        from src.settings import Settings as settings
        self.add_line(text, settings.BRED)

    def info(self, text):
        from src.settings import Settings as settings
        self.add_line(text, settings.WHITE)

    def note (self, text):
        from src.settings import Settings as settings
        self.add_line(text, settings.YELLOW)

    def add_line(self, text, color):
        self.lines.append((text, color))
        self.cur_line += 1

    def scroll(self, y):
        if y > 0:
            self.cur_line += 1
        elif y < 0:
            self.cur_line -= 1
        if self.cur_line < 0:
            self.cur_line = 0
        elif self.cur_line > len(self.lines):
            self.cur_line = len(self.lines)

