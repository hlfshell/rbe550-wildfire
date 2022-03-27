


from typing import Tuple
import pygame
from random import choice

tetrominoes = ["L", "L2", "T", "T2", "Z", "Z2",
    "I", "I2", "I3"]

def load_tetrominoe(sprite: str, sprite_burning: str) -> Tuple[pygame.Surface, pygame.Surface]:
    sprite = pygame.image.load(sprite).convert_alpha()
    burning_sprite = pygame.image.load(sprite_burning).convert_alpha()
    return sprite, burning_sprite

def grab_random_tetrominoe() -> Tuple[pygame.Surface, pygame.Surface]:
    prefix = "./wildfire/images/"
    tet = choice(tetrominoes)
    return load_tetrominoe(
        f"{prefix}/{tet}.png",
        f"{prefix}/{tet}_burning.png"
    )