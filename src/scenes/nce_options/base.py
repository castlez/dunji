import pygame

from src.engine import render
from src.settings import Settings as settings

class NCEOption:

    def __init__(self, name, prompt, choices, img):
        self.name = name
        self.prompt = prompt
        self.choices = choices
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.topleft = (235, 107)

        # prompt box
        prompt_y = 16
        self.prompt_img = pygame.image.load("src/sprites/ui/vert2.png")
        # determine prompt box size based on the longest line in the prompt
        prompt_x = 0
        for line in self.prompt:
            size = render.get_text_size(line)[0]
            if size > prompt_x:
                prompt_x = size
        # if self.prompt_pos[0] + prompt_x > settings.WIDTH:
        #     prompt_x = settings.WIDTH - self.prompt_pos[0]
        self.prompt_img = pygame.transform.scale(self.prompt_img, (prompt_x, 16*len(self.prompt)))
        self.prect = self.prompt_img.get_rect()
        self.prect.topleft = (settings.WIDTH - prompt_x - 5, prompt_y)

        # choices
        self.choice_ir = []  # choice (image, rects)
        for i, c in enumerate(self.choices):
            size_x = render.get_text_size(c)[0]
            size_y = render.get_text_size(c)[1] + 1
            img = pygame.image.load("src/sprites/ui/vert2.png")
            img = pygame.transform.scale(img, (size_x, size_y))
            rect = img.get_rect()
            base_y = self.prect.bottom + 2
            rect.topleft = (settings.WIDTH - size_x - 5, base_y + ((size_y+2)*i))

            self.choice_ir.append((img, rect))

    def update(self):
        for player in settings.players:
            player.update()

    def draw(self, screen):
        # event image
        screen.blit(self.img, self.rect.topleft)

        # prompt
        screen.blit(self.prompt_img, self.prect.topleft)
        for i, line in enumerate(self.prompt):
            render.render_text(line, (self.prect.topleft[0], self.prect.topleft[1] + 16*i))

        # choices
        for i, c in enumerate(self.choices):
            screen.blit(self.choice_ir[i][0], self.choice_ir[i][1].topleft)
            render.render_text(c, (self.choice_ir[i][1].topleft[0], self.choice_ir[i][1].topleft[1]))
