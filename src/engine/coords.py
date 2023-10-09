import math


def get_next_pos_towards( pos, dest, speed):
    # Find direction vector (dx, dy) between dest and pos.
    dx, dy = dest[0] - pos[0], dest[1] - pos[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return pos  # if already at location, freeze
    dx, dy = dx / dist, dy / dist  # Normalize

    # Move along this normalized vector away from the target
    return pos[0] + dx * speed, pos[1] + dy * speed


def get_new_dest_through(pos, target, max_x, max_y):
    """
    Draws a line through the given target from pos
    and returns the coordinates of the point where
    the line goes out of max range
    """
    dx, dy = target[0] - pos[0], target[1] - pos[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return pos  # if already at location, freeze
    dx, dy = dx / dist, dy / dist  # Normalize
    new_pos = pos
    while 0 < new_pos[0] < max_x and 0 < new_pos[1] < max_y:
        new_pos = new_pos[0] + dx, new_pos[1] + dy
    return new_pos


def distance(pos1, pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5