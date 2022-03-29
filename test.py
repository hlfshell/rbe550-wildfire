from random import randint
from time import sleep
from wildfire.game import Game
from wildfire.obstacle import Obstacle
from wildfire.prm import PRM

game = Game(
    (1250, 1250),
    5,
    time_per_second = 20.0
)
# obstacles = []
# for i in range(0, 15):
#     x = randint(0, 250)
#     y = randint(0, 250)
#     obstacles.append(Obstacle((x, y), 5))
# obstacles.sort(key = lambda x: x.xy[1])

# game.obstacles = obstacles
game.obstacle_fill(0.2)
game.render()
sleep(5)
game.generate_map()
game.loop()