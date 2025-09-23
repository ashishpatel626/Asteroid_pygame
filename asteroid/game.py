import pygame
from pygame.math import Vector2
from utils import load_sprite, get_random_position
from models import Spaceship, Asteroid

class asteroids():
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite('space', False)
        self.clock = pygame.time.Clock()

        self.spaceship = Spaceship(Vector2(400, 300))
        self.asteroids: list[Spaceship | Asteroid] = []

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if position.distance_to(self.spaceship.postion) > self.MIN_ASTEROID_DISTANCE:
                    break
            
            self.asteroids.append(Asteroid(position))
    
    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
        
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Asteroids")
    
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
        
        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_d]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_a]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_w]:
                self.spaceship.accelerate()

    def _process_game_logic(self):
        if self.spaceship:
            self.spaceship.move(self.screen)
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
        
        if self.spaceship:
            for asteroids in self.asteroids:
                if asteroids.collides_with(self.spaceship):
                    self.spaceship = None
                    break        

    def _draw(self):
        self.screen.blit(self.background, (0,0))
        if self.spaceship:
            self.spaceship.draw(self.screen)
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        
        pygame.display.flip()
        self.clock.tick(60)
    
    def _get_game_objects(self) -> list[Spaceship | Asteroid]:
        game_objects = [*self.asteroids]
        
        if self.spaceship:
            game_objects.append(self.spaceship)
        
        return game_objects