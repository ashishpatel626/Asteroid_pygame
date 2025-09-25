from pygame import Surface
from pygame.math import Vector2
from utils import load_sprite, wrap_position, get_random_velocity, load_sound
from pygame.transform import rotozoom
from typing import Callable

UP = Vector2(0, -1)

class GameObject:
    def __init__(self, position: Vector2, sprite: Surface, velocity: Vector2):
        self.postion = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity: Vector2 = Vector2(velocity)
        self.laser_sound = load_sound('laser')
        
    def draw(self, surface: Surface):
        blit_position = self.postion - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)
    
    def move(self, surface: Surface):
        self.postion = wrap_position(self.postion + self.velocity, surface)
    
    def collides_with(self, other_obj: 'GameObject'):
        distance = self.postion.distance_to(other_obj.postion)
        return distance < self.radius + other_obj.radius

class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 3

    def __init__(self, position: Vector2, create_bullet_callback: Callable[['Bullet'], None]):
        self.create_bullet_callback = create_bullet_callback
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite('spaceship'), Vector2(0))
    
    def rotate(self, clockwise: bool=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface: Surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.postion - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
    
    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
    
    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.postion, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()
    
class Asteroid(GameObject):
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self, position: Vector2, create_asteroid_callback: Callable[['Asteroid'], None], size: int=3):
        self.size = size
        self.create_asteroid_callback = create_asteroid_callback

        size_to_scale : dict[int, float] = {3: 1, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite('asteroid'), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1, 3))
    
    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(self.postion, self.create_asteroid_callback, self.size - 1)
                self.create_asteroid_callback(asteroid)


class Bullet(GameObject):
    def __init__(self, position: Vector2, velocity: Vector2):
        super().__init__(position, load_sprite('bullet'), velocity)
    
    def move(self, surface: Surface):
        self.postion = self.postion + self.velocity