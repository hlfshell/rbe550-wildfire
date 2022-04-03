from wildfire.game import Game

game = Game(
    (1250, 1250),
    5,
    time_per_second = 5.0
)

game.obstacle_fill(0.2)
game.create_vehicle()
game.render()
game.generate_map()

game.loop()