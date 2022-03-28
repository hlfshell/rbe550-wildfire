from __future__ import annotations
from math import pi

from math import degrees, floor
from typing import List
import pygame
from wildfire.obstacle import Obstacle

from wildfire.state import State


VEHICLE_SPRITE = "./wildfire/images/firetruck.png"
VEHICLE_SIZE = (2.3, 6.1)

class Vehicle(pygame.sprite.Sprite):

    def __init__(
        self,
        state: State,
        pixels_to_meter: int
    ):
        self.pixels_per_meter = pixels_to_meter
        self.state = state
        
        self.image : pygame.Surface = pygame.image.load(VEHICLE_SPRITE).convert_alpha()
        sprite_size = (VEHICLE_SIZE[0] * pixels_to_meter, VEHICLE_SIZE[1] * pixels_to_meter)
        self.image = pygame.transform.scale(self.image, (sprite_size[0], sprite_size[1]))

        self.surface : pygame.Surface = None

        self.path : List[State] = None
        self.path_time = 0.0
        self.path_time_delta = 0.0
        self.target_state : State = None

        self.render()

    def render(self):
        angle = -1*degrees(self.state.theta + (pi/2))
        self.surface = pygame.transform.rotate(self.image, angle)
        xy = (self.state.x * self.pixels_per_meter, self.state.y * self.pixels_per_meter)
        self.rect = self.surface.get_rect(center=xy)
        self.mask = pygame.mask.from_surface(self.surface)

    def blit(self, surface : pygame.Surface):
        surface.blit(self.surface, self.rect)
    
    def draw_path(self, surface : pygame.Surface):
        if self.path is None:
            return

        color = (255, 0, 0, 128)
        drawn = self.path.copy()
        first = drawn.pop(0)
        second  = drawn.pop(0)
        while True:
            firstxy = (first.x*self.pixels_per_meter, first.y*self.pixels_per_meter)
            secondxy = (second.x*self.pixels_per_meter, second.y*self.pixels_per_meter)
            pygame.draw.line(surface, color, firstxy, secondxy, width=3)
            first = second
            if len(drawn) == 0:
                break
            second = drawn.pop(0)
        pygame.display.update()

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

    def at_goal(self) -> bool:
        if self.path is None:
            return False
        
        return self.state == self.path[-1]

    def reset_path(self):
        self.path = None
        self.path_time = 0.0
        self.path_time_delta = 0.0

    def clone(self) -> Vehicle:
        state = self.state.clone()
        return Vehicle(state, self.pixels_per_meter)
    
    def tick(self, time_delta : float):

        if self.path is None:
            return

        self.path_time += time_delta

        # If we've reached our terminal state, just hold it
        if self.path_time >= self.path_time_delta * len(self.path):
            self.state = self.path[-1]
            return

        index = floor(self.path_time / self.path_time_delta)
        if index >= len(self.path):
            index = len(self.path) - 1

        # This is the current state whose dots we'll take
        state = self.path[index]

        xdelta = state.xdot * time_delta
        ydelta = state.ydot * time_delta
        thetadelta = state.thetadot * time_delta

        if thetadelta > pi:
            thetadelta = -1*((2*pi) - thetadelta)
        elif thetadelta < -pi:
            thetadelta = (2*pi) + thetadelta

        x = self.state.x + xdelta
        y = self.state.y + ydelta
        theta = self.state.theta + thetadelta

        self.state = State(
            (x, y),
            theta,
            self.state.psi,
            exact = True,
            xdot = state.xdot,
            ydot = state.ydot,
            thetadot = state.thetadot
        )