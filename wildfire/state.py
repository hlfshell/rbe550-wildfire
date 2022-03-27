from __future__ import annotations

from math import atan, cos, pi, radians, sin, sqrt, tan
from typing import List, Tuple

from numpy import arange

from wildfire.obstacle import Obstacle


class State:

    def __init__(
        self,
        xy: Tuple[float, float],
        theta: float,
        psi: float,
        exact=False,
        xdot=0.0,
        ydot=0.0,
        thetadot=0.0
    ):
        self.x = xy[0]
        self.y = xy[1]
        self.theta = theta

        self.theta = self.theta % (2*pi)
        if self.theta > pi:
            self.theta = -1*((2*pi) - self.theta)
        elif self.theta < pi:
            self.theta = (2*pi) + self.theta

        self.psi = psi
        if not exact:
            self.x = round(self.x, 1)
            self.y = round(self.y, 1)
            self.theta = round(self.theta, 1)
            self.psi = round(self.psi, 1)
        self.theta = self.theta % (2*pi)
        self.psi = self.psi  % (2*pi)

        self.xdot = xdot
        self.ydot = ydot
        self.thetadot = thetadot

        # Ackermann measurements
        self.width = 3 #meters
        self.length = 7 #meters
        self.L = 2.8 # wheelbase, meter
        self.psi_max = radians(60)
        self.max_velocity = 12 # meters / sec
    
    def get_neighbors(self, time_delta: float) -> List[State]:
        neighbors = []

        psi_increment = radians(15)

        for v in [-self.max_velocity, self.max_velocity]:
            for psi in arange(-self.psi_max, self.psi_max, psi_increment):
                state = self.forward_kinematics(v, psi, time_delta)
                if state.x < 0 or state.x > 250 or state.y < 0 or state.y > 250:
                    continue
                neighbors.append(state)

        return neighbors
    
    def forward_kinematics(self, v: float, psi: float, time_delta: float) -> State:
        thetadot = (v/self.L) * tan(psi)
        thetadelta = thetadot * time_delta
        thetadelta = thetadelta % (2*pi)
        if thetadelta > pi:
            thetadelta = (2*pi) - thetadelta
            thetadelta = -1 * thetadelta
        theta = self.theta + thetadelta
        xdot = v * cos(theta)
        xdelta = xdot * time_delta
        ydot = v * sin(theta)
        ydelta = ydot * time_delta

        x = self.x + xdelta
        y = self.y + ydelta

        return State(
            (x, y),
            theta,
            psi,
            xdot=xdot,
            ydot=ydot,
            thetadot=thetadot
        )

    def transition_cost(self, to: State) -> float:
        distance = self.distance_between(to)
        theta_difference = abs(self.theta - to.theta)
        if theta_difference > pi:
            theta_difference = (2*pi) - theta_difference
        return distance + (4*theta_difference)

    def distance_between(self, other: State) -> float:
        return sqrt((self.x-other.x)**2 + (self.y-other.y)**2)

    def obstacle_distance(self, obstacle: Obstacle) -> float:
        return sqrt((self.x-obstacle.xy[0])**2 + (self.y-obstacle.xy[1])**2)
    
    def connects(self, other: State, time_delta: float)-> State:
        distance = self.distance_between(other)
        max_distance = self.max_velocity * time_delta
        if distance > max_distance:
            return None
        
        thetadelta = self.theta - other.theta

        thetadotmax = (self.max_velocity/self.L) * tan(self.psi_max)
        thetadeltamax = abs(thetadotmax) * time_delta
        if abs(thetadelta) > thetadeltamax:
            return None
        
        theta = other.theta
        if theta == 0:
            theta = 0.001

        xdelta = self.x - other.x
        xdot = xdelta / time_delta
        ydelta = self.y - other.y
        ydot = ydelta / time_delta
        if xdelta != 0:
            v = xdot / cos(other.theta)
        else:
            v = ydot / sin(other.theta)

        if abs(v) > self.max_velocity:
            return None
        
        if xdelta != 0:
            psi = atan((thetadelta * self.L)/(xdelta/cos(theta)))
        else:
            psi = atan((thetadelta * self.L)/(ydelta/sin(theta)))
        
        psi = psi % (2*pi)
        if abs(psi) > pi:
            psi = -1*((2*pi) - abs(psi))

        if abs(psi) > self.psi_max:
            return None

        return other

    def clone(self) -> State:
        return State(
            (self.x, self.y),
            self.theta,
            self.psi,
            exact = True,
            xdot=self.xdot,
            ydot=self.ydot,
            thetadot=self.thetadot
        )
    
    def __eq__(self, other: State) -> bool:
        if other is None:
            return False
        distance = self.distance_between(other)
        theta_difference = abs(self.theta - other.theta)
        if theta_difference > pi:
            theta_difference = (2*pi) - theta_difference
        return distance < 0.5 and theta_difference < 0.1

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.theta))

    def __lt__(self, other: State) -> bool:
        return \
            (self.x, self.y, self.theta) < \
            (other.x, other.y, other.theta)