import math


class Coords:

    @classmethod
    def get_next_pos_towards(cls, pos, dest, speed):
        # Find direction vector (dx, dy) between dest and pos.
        dx, dy = dest[0] - pos[0], dest[1] - pos[1]
        dist = math.hypot(dx, dy)
        if dist == 0:
            return pos  # if already at location, freeze
        dx, dy = dx / dist, dy / dist  # Normalize

        # Move along this normalized vector away from the target
        return pos[0] + dx * speed, pos[1] + dy * speed

    @classmethod
    def distance(cls, pos1, pos2):
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5