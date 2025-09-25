import pygame
from pygame.math import Vector2
from utils import load_sprite, get_random_position, print_text
from models import Spaceship, Asteroid, Bullet

class asteroids():
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite('space', False)
        self.clock = pygame.time.Clock()
        self.asteroids: list[Asteroid] = []
        self.bullets: list[Bullet] = []
        self.spaceship = Spaceship(Vector2(400, 300), self.bullets.append)
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if position.distance_to(self.spaceship.postion) > self.MIN_ASTEROID_DISTANCE:
                    break
            
            self.asteroids.append(Asteroid(position, self.asteroids.append))
    
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
            
            if self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.spaceship.shoot()
        
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
                    self.message = 'You Lost!'
                    break     
        
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.postion):
                self.bullets.remove(bullet)
        
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break
        
        if not self.asteroids and self.spaceship:
            self.message = 'You Won!'

    def _draw(self):
        self.screen.blit(self.background, (0,0))
        if self.spaceship:
            self.spaceship.draw(self.screen)
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        
        if self.message:
            print_text(self.screen, self.message, self.font)
        
        pygame.display.flip()
        self.clock.tick(60)
    
    def _get_game_objects(self) -> list[ Bullet | Asteroid | Spaceship]:
        game_objects: list[Asteroid | Bullet | Spaceship] = [*self.asteroids, *self.bullets]
        
        if self.spaceship:
            game_objects.append(self.spaceship)
        
        return game_objects