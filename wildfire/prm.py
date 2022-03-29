from math import pi
from random import uniform
from typing import Callable, Tuple

import pygame
from sklearn.neighbors import KDTree
from wildfire.state import State

from wildfire.vehicle import Vehicle

class PRM():

    def __init__(
        self,
        size: Tuple[int, int],
        nodes_size: int,
        collision_detection: Callable,
        pixels_per_meter: int
    ):
        self.size = size
        self.nodes_size = nodes_size
        self.pixels_per_meter = pixels_per_meter
        self.kdtree = None
        self.collision_detection = collision_detection

    def generate(self):
        nodes = []
        while len(nodes) < self.nodes_size:
            x = uniform(0.0, self.size[0])
            y = uniform(0.0, self.size[1])
            theta = uniform(0.0, 2*pi)

            shadow_vehicle = Vehicle(State(
                (x, y),
                theta,
                0.0
            ), self.pixels_per_meter)

            # To prevent freezing complaints
            pygame.event.get()

            # Is it possible?
            if self.collision_detection(shadow_vehicle):
                continue

            nodes.append((x, y))

        self.kdtree = KDTree(nodes)


    def get_nodes_nearest(self, xy: Tuple[float, float], proximity : float):
        indexes = self.kdtree.query_radius(xy, r=proximity)
        return [self.kdtree.data[index] for index in indexes]

    def render(self, surface : pygame.Surface):
        if self.kdtree is None:
            return
        
        for datum in self.kdtree.data:
            xy = (datum[0]*self.pixels_per_meter, datum[1]*self.pixels_per_meter)
            pygame.draw.circle(surface, (92, 62, 240, 0.33), xy, 4)

    def search(self):
        pass