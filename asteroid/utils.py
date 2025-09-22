from pygame.image import load
from pathlib import Path
from pygame.math import Vector2
from pygame import Surface

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
