from random import randint
from time import sleep
from wildfire.game import Game
from wildfire.obstacle import Obstacle
from wildfire.prm import PRM

game = Game(
    (1250, 1250),
    5,
    time_per_second = 5.0
)

game.obstacle_fill(0.2)
game.create_vehicle()
game.render()

game.loop()