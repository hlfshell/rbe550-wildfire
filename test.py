from random import randint
from wildfire.game import Game
from wildfire.obstacle import Obstacle

game = Game(
    (1250, 1250),
    5
)

obstacles = []
for i in range(0, 15):
    x = randint(0, 250)
    y = randint(0, 250)
    obstacles.append(Obstacle((x, y), 5))
obstacles.sort(key = lambda x: x.xy[1])

game.obstacles = obstacles
game.loop()