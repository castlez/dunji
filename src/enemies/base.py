import pygame

from src.settings import Settings as settings


class Enemy(pygame.sprite.Sprite):
    # used for enemy placement
    sprite_layers = None  # list of sprite layers
    cr = 0  # challenge rating

    def __init__(self, pos, name, hp, damage, speed, description, sprite_layers):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.description = description
        self.img = pygame.image.load(f"src/sprites/{sprite_layers[0]}").convert_alpha()
        self.img_over = None
        if len(sprite_layers) > 1:
            self.img_over = pygame.image.load(f"src/sprites/{sprite_layers[1]}")

        self.rect = self.img.get_rect()
        self.rect.center = pos
        self.rect.center = pos

        if self.img_over:
            parray = pygame.PixelArray(self.img)
            # TODO do better coloring of enemies
            parray.replace(settings.WHITE, settings.GREY)
            self.img_over = pygame.image.load("src/sprites/baddies/bandit_over.png")

        self.turn_ptr = 0
        self.turn = ["move", "action", "done"]
        self.target = None
        self.traveled = 0  # distance travelled already this turn

        self.alive = True

    def take_turn(self):
        raise NotImplementedError()

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()

    def die(self):
        self.alive = False
        self.kill()

    def draw(self, screen):
        if not self.img:
            raise Exception("fuck 1")
        screen.blit(self.img, self.rect.center)
        if self.img_over:
            screen.blit(self.img_over, self.rect.center)

    def move(self, pos):
        # TODO do i need both of these?
        self.rect.center = pos
        self.rect.center = pos
