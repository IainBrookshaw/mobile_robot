#! /usr/bin/env python3
"""
Mobile Robot Path Planning: A* demonstration
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""
import matplotlib.pyplot as plt
from typing import Tuple
import numpy as np
import a_star
import maps

from planner import GridMapPlanner


def _generate_random_start(map: np.array, max_tries=100) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Keep trying until two clear points are located
    they are not guaranteed to be connected by a path
    """
    map_rows = map.shape[0]
    map_cols = map.shape[1]
    attempt = 0

    while True:
        start = (
            np.random.randint(low=0, high=map_rows-1),
            np.random.randint(low=0, high=map_cols-1)
        )
        goal = (
            np.random.randint(low=0, high=map_rows-1),
            np.random.randint(low=0, high=map_cols-1)
        )

        if 0 == map[start[0]][start[1]] and 0 == map[goal[0]][goal[1]]:
            break

        if attempt > max_tries:
            raise Exception(
                f"Could not find start or goal in {attempt} tries. Try another map")
        attempt += 1

    return (start, goal)


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    map_rows = 100
    map_cols = 100

    gridmap = maps.generate_random_obstacle_map(
        (map_rows, map_cols),
        obstacle="blob",
        obs_radius=10,
        obs_max=8,
        blur_sigma=0
    )
    start, goal = _generate_random_start(gridmap)

    print(f"A* demonstration\nMoving the robot from {start} to {goal}")
    planner = a_star.AStar()
    path = planner.plan(gridmap, start, goal)

    plottable_path = GridMapPlanner.marshal_pose_list_for_plot(path)
    plottable_visited = GridMapPlanner.marshal_pose_list_for_plot(
        planner.visited)

    plot = planner.plot_path(gridmap, plottable_path, plottable_visited)
    plt.show()
