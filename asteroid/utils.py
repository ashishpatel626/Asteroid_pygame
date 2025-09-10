from pygame.image import load
from pathlib import Path

def load_sprite(name: str, with_alpha: bool=True):
    path = Path(__file__).parent.parent/'assets'/'sprites'/f'{name}.png'

    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()