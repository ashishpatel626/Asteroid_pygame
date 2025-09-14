from pygame import Surface
from pygame.math import Vector2

class GameObject:
    def __init__(self, position: tuple[int, int], sprite: Surface, velocity: tuple[int, int]):
        self.postion = Vector2(position)
        self.spirte = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        
    def draw(self, surface: Surface):
        blit_position = self.postion - Vector2(self.radius)
        surface.blit(self.spirte, blit_position)
    
    def move(self):
        self.postion = self.postion + self.velocity
    
    def collides_with(self, other_obj: 'GameObject'):
        distance = self.postion.distance_to(other_obj.postion)
        return distance < self.radius + other_obj.radius
    