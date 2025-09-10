import pygame
from abc import abstractmethod
from utils import load_sprite

class asteroids():
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite('space', False)
    
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

    @abstractmethod
    def _process_game_logic(self):
        # pygame.sprite.collide_circle()
        pass

    def _draw(self):
         self.screen.blit(self.background, (0,0))
         pygame.display.flip()