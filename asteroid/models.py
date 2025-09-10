from pygame.math import Vector2
from pygame import Surface

class GameObject:
    def __init__(self, position: int, sprite: Surface, velocity: int):
        self.postion = Vector2(position)
        self.spirte = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        