# RBE 550 Wildfire

<img src="docs/imgs/RBE550 Valet flow chart.png" width=300/>
<img src="videos/astar.gif" width=300/>
<img src="videos/prm.gif" width=300/>

This is the repository for my RBE550 Wildfire assignment. In a simulation that can run at faster speeds (ie one second == 5 seconds or more), simulate an automated Mercedes fire truck with ackermann steering. An arsonist is routinely lighting fires to trees in the environment, which in turn spreads at a set interval to nearby trees.

This simulation can be ran with either a local planner alone, or a local planner and a global planner.

The global planner utilizes a PRM (probabilistic road map) that is generate at the onset of the program. It creates thousands of random positions, where the firetruck is positioned in a random orientation, and checks for collissions. If none are present, it will mark it as a potential node with the PRM. Nodes are kept in a KD-tree courtesy of `sklearn`. When the global planner needs to navigate from the given location to a fire, we first find the closest node to the fire truck, and then the closest node to the fire. It then utilizes A* moving through nodes, with euclidean distance as the heuristic.

The local planner either plans between desired nodes of the PRM or between the goal and start location, depending on if the global planner was utilized or not. The local planner is still A*, but explores the continuous space by utilizing kinematic primitives from the ackermann stle chasis of the robot in question - thus all planned movements are technically possible given the defined constraints of the platform.

The written explainer for the assignment can be found in `docs/report.pdf`.

This project can be ran via

```
python run.py
```

...which will run the simulator for the A* planner and then the PRM planner. To run just one, you can utilize `python astar.py` or `python prm.py` respectively.

All planners can be found in `wildfire/planner.py`; the PRM implementation in `wildfire/prm.py`. Vehicle dynamics are in `wildfire/state.py` with the vehicle in-game state controlled via `wildfire/vehicle.py`.