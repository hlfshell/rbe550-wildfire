from math import floor, pi
from random import choice, randint, random
from secrets import randbits
from typing import List, Tuple
import pygame

from wildfire.obstacle import BURNING, EXTINGUISHED, Obstacle
from wildfire.planner import Planner
from wildfire.state import State
from wildfire.vehicle import Vehicle

BG_SPRITE = "./wildfire/images/grass.png"
BG_SIZE = (685, 460)
GOAL_PROXIMITY = 10.0
IGNITE_PROXIMITY = 30.0
SPREAD_SECONDS = 60.0
IGNITE_SECONDS = 20.0


class Game:

    def __init__(
        self,
        window_size: Tuple[int, int],
        pixels_per_meter: int,
        time_per_second: float = 1.0,
    ):
        self.window_size = window_size
        self.pixels_per_meter = pixels_per_meter
        self._display_surface : pygame.Surface = None
        self._frame_per_sec = pygame.time.Clock()
        self._fps = 60

        self.obstacles : List[Obstacle] = []
        self.unreachable_obstacles : List[Obstacle] = []
        self.goal = None

        self.time_per_frame = time_per_second / self._fps

        self.time = 0.0
        self.last_ignite = 0.0
        
        self._display_surface = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Wildfire")

        self.bg_sprite = pygame.image.load(BG_SPRITE).convert_alpha()
        self.bg_sprite = pygame.transform.scale(self.bg_sprite, BG_SIZE)

        self.vehicle : Vehicle = None
        self.create_vehicle()

        self.render()

    def obstacle_percentage(self) -> float:
        w, h = self._display_surface.get_size()
        total_pixels = w*h
        obstacle_pixels = 0
        for obstacle in self.obstacles:
            obstacle_pixels += obstacle.pixel_count
        
        return obstacle_pixels / total_pixels

    def obstacle_fill(self, percentage : float):
        while True:
            if self.obstacle_percentage() >= percentage:
                self.obstacles.sort(key = lambda o: o.xy[1])
                return
            
            x = randint(0, 250)
            y = randint(0, 250)
            self.obstacles.append(Obstacle((x, y), self.pixels_per_meter))

    def create_vehicle(self):
        while self.vehicle is None:
            x = randint(0, 250)
            y = randint(0, 250)
            theta = random() * pi
            if randbits(1):
                theta = -theta

            vehicle = Vehicle(State(
                (x, y),
                theta,
                0.0
            ), self.pixels_per_meter)

            if not self.collision_detection(vehicle):
                self.vehicle = vehicle

    def generate_obstacles(self, fill_percentage : float):
        iterations = 0
        max_iterations = 1_000
        while self.obstacle_percentage() < fill_percentage:
            iterations += 1
            if iterations > max_iterations:
                raise Exception("Can not fill map to sufficient percentage")
            try:
                self.add_random_obstacle()
            except:
                continue

    def render(self):
        # Draw background
        pygame.Surface.fill(self._display_surface, (0, 0, 0))
        for w in range(0, 3):
            for h in range(0, 3):
                w_center = (w * (BG_SIZE[0] - 20)) + floor(BG_SIZE[0]/2) - 10
                h_center = (h * (BG_SIZE[1] - 20)) + floor(BG_SIZE[1]/2) - 10
                tile_surface = self.bg_sprite.copy()
                tile_rect = tile_surface.get_rect(center=(w_center, h_center))
                self._display_surface.blit(tile_surface, tile_rect)

        for obstacle in self.obstacles:
            obstacle.render()
            self._display_surface.blit(obstacle.surface, obstacle.rect)
        
        if self.vehicle is not None:
            self.vehicle.draw_path(self._display_surface)
            self.vehicle.render()
            self.vehicle.blit(self._display_surface)

        pygame.display.update()

    def collision_detection(self, vehicle : Vehicle) -> bool:
        for obstacle in self.obstacles:
            if vehicle.collision_check(obstacle):
                return True
        return False

    def tick(self):
        if self.goal is None and self.vehicle.path is None:
            burning_obstacles = self.obstacles_by_state(BURNING)
            burning_obstacles = [
                    o for o \
                        in burning_obstacles \
                        if o not in self.unreachable_obstacles
                ]
            if len(burning_obstacles) > 0:
                burning_obstacles.sort(
                    key=lambda o: self.vehicle.state.obstacle_distance(o)
                )
                chosen_obstacle = burning_obstacles[0]
                self.goal = chosen_obstacle.xy
                planner_time_delta = 0.25
            
                self.planner = Planner(
                    self.vehicle.state,
                    self.goal,
                    GOAL_PROXIMITY,
                    planner_time_delta,
                    self.collision_detection,
                    self._display_surface,
                    self.pixels_per_meter
                )

                try:
                    path = self.planner.search()
                    self.unreachable_obstacles = []
                    self.vehicle.path = path
                    self.vehicle.path_time_delta = planner_time_delta
                except Exception as e:
                    # raise e
                    print("Could not solve path")
                    self.goal = None
                    self.unreachable_obstacles.append(chosen_obstacle)
        
        for obstacle in self.obstacles:
            obstacle.tick(self.time_per_frame)
        
        for obstacle in self.obstacles_by_state(BURNING):
            if obstacle.burning_for - obstacle.last_neighbor_ignition >= SPREAD_SECONDS:
                obstacle.last_neighbor_ignition = obstacle.burning_for
                to_ignite = self.obstacles_within_range(obstacle, IGNITE_PROXIMITY)
                for ignite in to_ignite:
                    if ignite != obstacle:
                        ignite.ignite()
        
        self.vehicle.tick(self.time_per_frame)

        if self.time > self.last_ignite + IGNITE_SECONDS or self.time == 0.0:
            self.last_ignite = self.time
            extinguished_obstacles = self.obstacles_by_state(EXTINGUISHED)
            if len(extinguished_obstacles) > 0:
                obstacle : Obstacle = choice(extinguished_obstacles)
                obstacle.ignite()
        
        if self.vehicle.at_goal():
            goal_obstacle = [o for o in self.obstacles if o.xy == self.goal][0]
            goal_obstacle.extinguish()
            self.goal = None
            self.vehicle.reset_path()

        self.time += self.time_per_frame

    def loop(self):
        self.last_ignite = 0.0

        while True:
            self.render()
            self.tick()
            pygame.event.get() # To prevent feezing, get input events
            self._frame_per_sec.tick(self._fps)

    def plan(self):
        pass

    def animate_path(self, path: List[State]):
        pass

    def draw_path(self, path: List[State]):
        pass

    def obstacles_by_state(self, state: int):
        return [obstacle for obstacle in self.obstacles if obstacle.state == state]
    
    def obstacles_within_range(self, obstacle: Obstacle, range : float) -> List[Obstacle]:
        return [
            other for other in self.obstacles
            if obstacle.distance_between(other) <= range
        ]