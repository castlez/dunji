import pygame

class Enemy(pygame.sprite.Sprite):
    # used for enemy placement
    sprite_layers = None  # list of sprite layers
    cr = 0  # challenge rating

    def __init__(self, pos, name, hp, damage, speed, description):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.description = description
        self.pos = pos
        self.img_base = None
        self.img_over = None

        self.turn_ptr = 0
        self.turn = ["move", "action", "done"]
        self.target = None
        self.traveled = 0  # distance travelled already this turn

    def take_turn(self):
        raise NotImplementedError()

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()

    def die(self):
        raise NotImplementedError()

    def draw(self, screen):
        if not self.img_base or not self.img_over:
            raise Exception("fuck 1")
        screen.blit(self.img_base, self.pos)
        screen.blit(self.img_over, self.pos)
