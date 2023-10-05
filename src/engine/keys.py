import pygame
from src.settings import Settings as settings
keys_down = []


def get(key, up=True):
    parts = key.split("+")
    check = parts[-1]
    if len(parts) > 1:
        mod = parts[0]
        if mod == "ctrl":
            if not pygame.key.get_mods() & pygame.KMOD_CTRL:
                return False
        elif mod == "shift":
            if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                return False
        elif mod == "alt":
            if not pygame.key.get_mods() & pygame.KMOD_ALT:
                return False
    check_type = pygame.KEYUP if up else pygame.KEYDOWN

    # reset k_check to be pygame.SPACE if it's "space"
    if key == "space":
        check = pygame.K_SPACE
    else:
        check = getattr(pygame, f"K_{check}")
    for event in settings.events:
        if event.type == check_type:
            if event.key == check:
                return True
    return False


def get_number_key():
    for i in range(10):
        if pygame.key.get_pressed()[getattr(pygame, f"K_{i}")]:
            return i
    else:
        return None


def reset():
    global keys_down
    keys_down = []
