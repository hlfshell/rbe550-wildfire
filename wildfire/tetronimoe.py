


from typing import Tuple
import pygame
from random import choice

tetrominoes = [
    ("L", (30, 45)),
    ("L2", (30, 45)),
    ("T", (45, 30)),
    ("T2", (45, 30)),
    ("Z", (45, 30)),
    ("Z2", (45, 30)),
    ("I", (15, 60)),
    # ("I2", (15, 60)),
    # ("I3", (15, 60))
    ]

def load_tetrominoe(
    sprite: str,
    sprite_burning: str,
    size : Tuple[int, int],
    pixels_per_meter : float
    ) -> Tuple[pygame.Surface, pygame.Surface]:
    sprite = pygame.image.load(sprite).convert_alpha()
    burning_sprite = pygame.image.load(sprite_burning).convert_alpha()

    # pixel_size = (size[0] * pixels_per_meter, size[1] * pixels_per_meter)
    pixel_size = (15* pixels_per_meter, 15*pixels_per_meter)

    sprite = pygame.transform.scale(sprite, pixel_size)
    burning_sprite = pygame.transform.scale(burning_sprite, pixel_size)

    return sprite, burning_sprite

def grab_random_tetrominoe(pixels_per_meter : float) -> Tuple[pygame.Surface, pygame.Surface]:
    prefix = "./wildfire/images/"
    shape, size = choice(tetrominoes)
    
    return load_tetrominoe(
        f"{prefix}/{shape}.png",
        f"{prefix}/{shape}_burning.png",
        size,
        pixels_per_meter
    )