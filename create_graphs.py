from matplotlib import pyplot as plt
import csv

ASTAR = "astar"
PRM = "prm"

paths = {}
fires = {}
intact = {}

# Read in 5 runs worth of data
for planner_type in [ASTAR, PRM]:
    paths[planner_type] = {}
    fires[planner_type] = {}
    intact[planner_type] = {}

    for run in range(1, 5+1):
        paths_f = open(f"./runs/paths_{planner_type}_{run}.csv")
        fires_f = open(f"./runs/fires_{planner_type}_{run}.csv")
        intact_f = open(f"./runs/intact_{planner_type}_{run}.csv")

        paths_reader = csv.reader(paths_f)
        fires_reader = csv.reader(fires_f)
        intact_reader = csv.reader(intact_f)

        paths[planner_type][run] = [row for row in paths_reader]
        fires[planner_type][run] = [row for row in fires_reader]
        intact[planner_type][run] = [row for row in intact_reader]

# From this begin building our plots

## PATHS
plt.figure("astar_paths")
plt.title("A* Path generation time by distance")
plt.xlabel("Distance to Goal (meters)")
plt.ylabel("Time to find path (seconds)")
all = []
for run in range(1, 5+1):
    all += paths[ASTAR][run]
all.sort(key=lambda x: x[1])
plt.plot(
    [float(t[1]) for t in all],
    [float(t[0])/1_000_000_000 for t in all],
    "o"
)
plt.savefig("./plots/astar_paths.jpg")

plt.figure("prm_paths")
plt.title("PRM + A* Path generation time by distance")
plt.xlabel("Distance to Goal (meters)")
plt.ylabel("Time to find path (seconds)")
all = []
for run in range(1, 5+1):
    all += paths[PRM][run]
all.sort(key=lambda x: x[1])
plt.plot(
    [float(t[1]) for t in all],
    [float(t[0])/1_000_000_000 for t in all],
    "o"
)
plt.savefig("./plots/prm_paths.jpg")

## FIRE AND INTACT
plt.figure("astar_fires")
plt.title("A* Obstacle Burning Percentage over Time")
plt.xlabel("Time")
plt.ylabel("Percentage of Obstacles Burning")
for run in range(1, 5+1):
    plt.plot(
        [float(t[0]) for t in fires[ASTAR][run]],
        [float(t[1])*100 for t in fires[ASTAR][run]],
        ".",
        label=f"Run {run}"
    )
plt.legend(loc="upper left")
plt.savefig("./plots/astar_obstacles_burning.jpg")

plt.figure("astar_intact")
plt.title("A* Obstacles Intact Percentage Over Time")
plt.xlabel("Time")
plt.ylabel("Percentage of Obstacles Intact")
for run in range(1, 5+1):
    plt.plot(
        [float(t[0]) for t in intact[ASTAR][run]],
        [float(t[1])*100 for t in intact[ASTAR][run]],
        label=f"Run {run}"
    )
plt.legend(loc="upper right")
plt.savefig("./plots/astar_obstacles_intact.jpg")

# PRM
plt.figure("prm_fires")
plt.title("PRM + A* Obstacle Burning Percentage over Time")
plt.xlabel("Time")
plt.ylabel("Percentage of Obstacles Burning")
for run in range(1, 5+1):
    plt.plot(
        [float(t[0]) for t in fires[PRM][run]],
        [float(t[1])*100 for t in fires[PRM][run]],
        ".",
        label=f"Run {run}"
    )
plt.legend(loc="upper left")
plt.savefig("./plots/prm_obstacles_burning.jpg")

plt.figure("prm_intact")
plt.title("PRM + A* Obstacles Intact Percentage Over Time")
plt.xlabel("Time")
plt.ylabel("Percentage of Obstacles Intact")
for run in range(1, 5+1):
    plt.plot(
        [float(t[0]) for t in intact[PRM][run]],
        [float(t[1])*100 for t in intact[PRM][run]],
        label=f"Run {run}"
    )
plt.legend(loc="upper right")
plt.savefig("./plots/prm_obstacles_intact.jpg")