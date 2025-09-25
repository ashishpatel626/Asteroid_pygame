from pygame.image import load
from pathlib import Path
from pygame.math import Vector2
from pygame import Surface, Color
import random
from pygame.mixer import Sound
from pygame.font import Font

def load_sprite(name: str, with_alpha: bool=True):
    path = Path(__file__).parent.parent/'assets'/'sprites'/f'{name}.png'

    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()

def wrap_position(position: Vector2, surface: Surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)

def get_random_position(surface: Surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height())
    )

def get_random_velocity(min_speed: int, max_speed: int):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)

def load_sound(name: str):
    path = Path(__file__).parent.parent/'assets'/'sounds'/f'{name}.wav'
    return Sound(path)

def print_text(surface: Surface, text: str, font: Font, color: Color = Color('tomato')):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    size = surface.get_size()
    rect.center = (int(size[0] / 2), int(size[1] / 2))
    surface.blit(text_surface, rect)