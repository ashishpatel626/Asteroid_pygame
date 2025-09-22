from pygame import Surface
from pygame.math import Vector2
from utils import load_sprite, wrap_position
from typing import Any
from pygame.transform import rotozoom

UP = Vector2(0, -1)

class GameObject:
    def __init__(self, position: tuple[int, int], sprite: Surface, velocity: Any):
        self.postion = Vector2(position)
        self.spirte = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        
    def draw(self, surface: Surface):
        blit_position = self.postion - Vector2(self.radius)
        surface.blit(self.spirte, blit_position)
    
    def move(self, surface: Surface):
        self.postion = wrap_position(self.postion + self.velocity, surface)
    
    def collides_with(self, other_obj: 'GameObject'):
        distance = self.postion.distance_to(other_obj.postion)
        return distance < self.radius + other_obj.radius

class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25

    def __init__(self, position: tuple[int, int]):
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite('spaceship'), Vector2(0))
    
    def rotate(self, clockwise: bool=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface: Surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.spirte, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.postion - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
    
    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION