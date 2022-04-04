# RBE 550 Wildfire

This is the repository for my RBE550 Wildfire project.

The written explainer for the assignment can be found in `docs/report.pdf`.

This project can be ran via

```
python run.py
```

...which will run the simulator for the A* planner and then the PRM planner. To run just one, you can utilize `python astar.py` or `python prm.py` respectively.

All planners can be found in `wildfire/planner.py`; the PRM implementation in `wildfire/prm.py`. Vehicle dynamics are in `wildfire/state.py` with the vehicle in-game state controlled via `wildfire/vehicle.py`.