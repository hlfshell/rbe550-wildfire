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
        self.kdtree : KDTree = None
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
        self.nodes = nodes
        self.kdtree = KDTree(nodes)

    def get_nodes_within_range(self, xy: Tuple[float, float], proximity : float, count = None):
        indexes, _ = self.kdtree.query_radius(
            [xy],
            r=proximity,
            return_distance=True,
            sort_results=True
        )
        results = [self.nodes[index] for index in indexes[0]]
        if count is not None:
            results = results[0:count-1]
        return results

    def get_nodes_nearest(self, xy: Tuple[float, float], k : int):
        _, indexes = self.kdtree.query([xy], k=k)
        return [self.nodes[index] for index in indexes[0]]

    def render(self, surface : pygame.Surface):
        if self.kdtree is None:
            return
        
        for datum in self.kdtree.data:
            xy = (datum[0]*self.pixels_per_meter, datum[1]*self.pixels_per_meter)
            pygame.draw.circle(surface, (92, 62, 240, 0.1), xy, 3)

    def search(self):
        pass