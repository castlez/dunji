import pygame
from src.settings import Settings as settings

keys_down = []


def get( key, once=False):
    parts = key.split("+")
    k_check = parts[-1]
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

    if pygame.key.get_pressed()[getattr(pygame, f"K_{k_check.lower()}")]:
        return True


def get_number_key():
    for i in range(10):
        if pygame.key.get_pressed()[getattr(pygame, f"K_{i}")]:
            return i
    else:
        return None


def reset():
    global keys_down
    keys_down = []
