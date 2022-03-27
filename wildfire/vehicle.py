from __future__ import annotations

from math import degrees, floor
from typing import List
import pygame
from wildfire.obstacle import Obstacle

from wildfire.state import State


VEHICLE_SPRITE = "./wildfire/images/firetruck.png"

class Vehicle(pygame.sprite.Sprite):

    def __init__(
        self,
        state: State,
        pixels_to_meter: int
    ):
        self.pixels_per_meter = pixels_to_meter
        self.state = state
        self.image_shape = (137, 100)
        self.image : pygame.Surface = pygame.image.load(VEHICLE_SPRITE).convert_alpha()
        self.surface : pygame.Surface = None

        self.path : List[State] = None
        self.path_time = 0.0
        self.target_state : State = None

        self.render()
    
    def render(self):
        self.surface = pygame.transform.rotate(self.image, -1*degrees(self.state.theta))
        xy = (self.state.x * self.pixels_per_meter, self.state.y * self.pixels_per_meter)
        self.rect = self.surface.get_rect(center=xy)
        self.mask = pygame.mask.from_surface(self.surface)

    def blit(self, surface : pygame.Surface):
        surface.blit(self.surface, self.rect)
    
    def collision_check(self, obstacle : Obstacle):
        # First we test the rects - if they overlap,
        # we can then spend the time doing a finer degree
        # of checking 
        if obstacle.rect.colliderect(self.rect):
            offset = (self.rect[0] - obstacle.rect[0], self.rect[1] - obstacle.rect[1])
            obstacle_mask = pygame.mask.from_surface(obstacle.surface)
            collisions = obstacle_mask.overlap(self.mask, offset)
            if collisions is not None and len(collisions) > 0:
                return True

        return False
    
    def clone(self) -> Vehicle:
        state = self.state.clone()
        return Vehicle(state, self.pixels_per_meter)
    
    def tick(self, time_delta : float):

        if self.path is None:
            return

        self.path_time += time_delta

        # TODO - Make this smoother you dumb dumb
        # get the lowest increment of 0.5
        index = floor(self.path_time / 0.5)

        self.state = self.path[index]