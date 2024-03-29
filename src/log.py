import pygame.sprite
import re


class Log(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.log_box_size = (200, 70)
        self.img = pygame.image.load("src/sprites/ui/vert.png")
        self.img = pygame.transform.scale(self.img, self.log_box_size)
        self.rect = self.img.get_rect()
        self.rect.topleft = pos
        self.show = False
        self.show_lines = 6  # how many lines to show
        self.viewed_lines = []
        self.size = 10

        self.lines = []
        self.cur_line = 0

    def startup_log(self):
        # prepopulate with some lines
        self.good("Welcome to Dunji!")
        self.good("As the DM, guide your party")
        self.good("5 sessions in a campaign")
        self.good("5 encounters per session")
        self.good("Good luck!")
        self.note("('h' for help, 'l' for log)")
        self.info("this is a super long log message that will hopefully result in wrapping at least twice")

    def set_pos(self, pos):
        self.rect.topleft = pos

    def update(self):
        from src.settings import Settings as settings
        if self.cur_line - self.show_lines < 0:
            begin = 0
        else:
            begin = self.cur_line - self.show_lines
        self.viewed_lines = self.lines[begin:self.cur_line]
        box_height = self.img.get_height() * settings.SCALEFACTOR
        self.size = 9  # boo magic numbers everywhere

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
            size = box_height // self.show_lines - 2  # boo magic numbers everywhere
            buff = size // 2.5
            for line in lines:
                if "|" in line[0]:
                    # player line needs fancy coloring
                    # "Witch|255,255,255|has stolen your gold!"
                    parts = line[0].split("|")
                    pc = parts[0]
                    cparts = parts[1].split(",")
                    color = (int(cparts[0]), int(cparts[1]), int(cparts[2]))
                    msg = parts[2].strip()
                    # split dist is the distance between the name and the text itself
                    split_dist = render.get_text_size(pc)[0]
                    render.render_text(pc, (cur_x, cur_y), color=color, size=size, scaled=True)
                    render.render_text(msg, (cur_x + split_dist, cur_y),
                                       color=line[1], size=size, scaled=True)
                else:
                    text = line[0]
                    render.render_text(text, (cur_x, cur_y), color=line[1], size=size, scaled=True)
                cur_y += buff

    def good(self, text, source=None):
        from src.settings import Settings as settings
        self.add_line(text, settings.BGREEN, source=source)

    def bad(self, text, source=None):
        from src.settings import Settings as settings
        self.add_line(text, settings.BRED, source=source)

    def info(self, text, source=None):
        from src.settings import Settings as settings
        self.add_line(text, settings.WHITE, source=source)

    def note(self, text, source=None):
        from src.settings import Settings as settings
        self.add_line(text, settings.YELLOW, source=source)

    def add_line(self, text, color, source=None):
        from src.engine import render
        from textwrap import wrap
        from src.settings import Settings as settings

        if source:
            text = (f"{source.name}|"
                    f"{source.color[0]},{source.color[1]},{source.color[2]}|"
                    f"{text}")

        # cut the text into sections so it doesn't
        # overflow the text box

        ctext = text
        if source:
            parts = text.split("|")
            ctext = parts[0] + " " + parts[2]
        char_size = render.get_text_size("a", scaled=True)[0]
        max_len = (self.log_box_size[0] * settings.SCALEFACTOR) // char_size
        text_length = render.get_text_size(ctext, scaled=True)[0]
        max_len = min(max_len, text_length)
        max_len = 34  # TODO this is (text_length // 7.9) for some reason
        sections = wrap(ctext, max_len)
        for i, section in enumerate(sections):
            if source:
                if i == 0:
                    # add the color back in
                    s = source.name
                    c = f"{source.color[0]},{source.color[1]},{source.color[2]}"
                    t = section[len(s):]
                    section = "|".join([s, c, t])
                else:
                    spaces = int(len(source.name))
                    section = f"{spaces * ' '}{section}"
            self.lines.append((section, color))
            print(section)
        self.cur_line += len(sections)

    def scroll(self, y):
        if y > 0:
            self.cur_line += 1
        elif y < 0:
            self.cur_line -= 1
        if self.cur_line < 0:
            self.cur_line = 0
        elif self.cur_line > len(self.lines):
            self.cur_line = len(self.lines)

