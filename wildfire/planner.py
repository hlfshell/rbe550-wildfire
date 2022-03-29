


from collections import defaultdict
from math import degrees, sqrt
from queue import PriorityQueue
from typing import Callable, Dict, List, Optional, Tuple
from numpy import arange

import pygame
from wildfire.prm import PRM

from wildfire.state import State
from wildfire.vehicle import Vehicle


MAX_STEPS = 5_000
MAX_X = 1250
MAX_Y = 1250

class Planner():

    def __init__(
        self,
        initial_state: State,
        goal: Tuple[float, float],
        proximity: float,
        time_delta: float,
        collision_detection: Callable,
        display: pygame.Surface,
        pixels_per_meter: float
    ):
        self.start = initial_state
        self.goal = goal
        self.queue = AStar()
        self.steps_taken = 0
        self.time_delta = time_delta
        self.proximity = proximity
        self.pixels_per_meter = pixels_per_meter
        self.display = display
        
        self.parents : Dict[State, State] = {}
        self.exists = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(
                    lambda: False
                )
        ))

        self.costs : Dict[State, float] = {}
        self.costs[self.start] = 0
        self.collision_detection = collision_detection

    def goal_distance(self, state : State) -> float:
        return sqrt(
            (state.x - self.goal[0])**2 +
            (state.y - self.goal[1])**2
        )

    def search(self) -> List[State]:
        path: Optional[List[State]] = None
        self.queue.push(self.start)

        while path == None:
            path = self.step()
            # This is here to avoid freezing warnings
            # for the window while calculating paths
            pygame.event.get()
            pygame.display.update()
        
        return path
    
    def step(self) -> Optional[List[State]]:
        self.steps_taken += 1
        if self.steps_taken == MAX_STEPS:
            raise "Excessive search steps to discover path"
        
        if len(self.queue) == 0:
            raise Exception("No path to the goal exists")
        
        # Get the next candidate from our current state
        current = self.queue.pop()

        #???? TODO: Short hop check?

        # If our current state is our goal state, we've hit our
        # goal, we're done! Let's build the path...
        if self.goal_distance(current) < self.proximity:
            if current == self.start:
                return [current]
            path: List[State] = [current]
            while True:
                current : State = self.parents[current]
                path.insert(0, current)
                if self.start == current:
                    return path

        # Get each neighbor for the current State and queue
        # them. First, we get a list of potential neighbors
        # that are valid from the current state - this
        # excludes any potential kinematic constraints for
        # the robot itself. We then move through each
        # neighbor and confirm that it does not cause a
        # collision. If it doesn't, we see if it's a neighbor
        # we've considered before. If so, we ignore it. If
        # not, we add it to our queue to consider,
        # calculating its total cost, which includes the
        # heuristic cost as well.
        neighbors = current.get_neighbors(self.time_delta)
        for neighbor in neighbors:
            if neighbor.x < 0 or neighbor.y < 0:
                continue
            if neighbor.x > (MAX_X/self.pixels_per_meter) or \
                neighbor.y > (MAX_Y/self.pixels_per_meter):
                continue

            # If we have already reached this state, we don't
            # need to retread over this ground
            x = round(0.5 * round(neighbor.x/0.5),2)
            y = round(0.5 * round(neighbor.y/0.5),2)
            theta = round(degrees(10) * round(neighbor.theta/degrees(10)),2)
            # if neighbor not in self.parents:
            if not self.exists[x][y][theta]:
                # Collisions detection
                shadow = Vehicle(neighbor, self.pixels_per_meter)
                if self.collision_detection(shadow):
                    continue

                self.parents[neighbor] = current
                self.exists[x][y][theta] = True

                # Calculate our costs
                if self.start == current:
                    current_cost = 0
                else:
                    current_cost = self.costs[current]

                distance_to_goal = self.goal_distance(neighbor)
                heuristic_cost = 10 * distance_to_goal

                node_cost = current_cost + current.transition_cost(neighbor)

                total_cost = node_cost + heuristic_cost
                self.costs[neighbor] = node_cost

                self.queue.push(neighbor, total_cost)
    
            # Draw a dot for the current considered spot
            pos = (neighbor.x, neighbor.y)
            pos = (pos[0]*self.pixels_per_meter, pos[1]*self.pixels_per_meter)
            self.display.fill((255, 255, 255), (pos, (2, 2)))


class AStar():

    def __init__(self):
        self.queue = PriorityQueue()
    
    def push(self, state: State, cost=0):
        self.queue.put((cost, state))

    def pop(self) -> State:
        return self.queue.get()[1]

    def __len__(self):
        return len(self.queue.queue)