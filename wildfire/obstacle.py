from __future__ import annotations
from math import sqrt
from secrets import randbits
from typing import Tuple
import pygame

from wildfire.tetronimoe import grab_random_tetrominoe

EXTINGUISHED = 0
BURNING = 1

class Obstacle():

    def __init__(self, xy : Tuple[float, float], pixels_per_meter : float):
        self.xy = xy
        self.pixels_per_meter = pixels_per_meter
        sprite, burning_sprite = grab_random_tetrominoe(pixels_per_meter)
        self.sprite = sprite
        self.burning_sprite = burning_sprite

        if bool(randbits(1)):
            self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.burning_sprite = pygame.transform.flip(self.burning_sprite, True, False)
        
        self.surface = self.sprite
        self.pixel_xy = (
            xy[0] * self.pixels_per_meter,
            xy[1] * self.pixels_per_meter
        )
        self.rect = self.surface.get_rect(center=self.pixel_xy)

        self.state = EXTINGUISHED
        self.burning_for = 0.0
        self.last_neighbor_ignition = 0.0
        self.has_burned = False

        self.pixel_count = self.get_obstacle_pixel_count()

        self.render()
    
    def get_obstacle_pixel_count(self) -> int:
        pixel_count = 0
        w, h = self.sprite.get_size()
        for x in range(0, w):
            for y in range(0, h):
                rgba = self.sprite.get_at((x, y))
                if rgba.a == 255:
                    pixel_count += 1
        return pixel_count

    def render(self):
        if self.state == BURNING:
            self.surface = self.burning_sprite
        else:
            self.surface = self.sprite
    
    def blit(self, surface : pygame.Surface):
        surface.blit(self.surface, self.rect)
    
    def ignite(self):
        if self.state == BURNING:
            return
        
        self.state = BURNING
        self.burning_for = 0.0
        self.last_neighbor_ignition = 0.0
        self.has_burned = True
    
    def extinguish(self):
        self.state = EXTINGUISHED
        self.burning_for = 0.0
        self.last_neighbor_ignition = 0.0
    
    def reset(self):
        self.extinguish()
        self.has_burned = False

    def distance_between(self, other: Obstacle) -> float:
        return sqrt(
            (self.xy[0]-other.xy[0])**2 +
            (self.xy[1]-other.xy[1])**2
        )

    def tick(self, time_delta : float):
        if self.state == EXTINGUISHED:
            return
        
        self.burning_for += time_delta