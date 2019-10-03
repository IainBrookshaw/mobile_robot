#! /usr/bin/env python3
"""
Mobile Robot Path Planning: A* demonstration
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""
import matplotlib.pyplot as plt
import numpy as np
import time

from typing import Tuple

from path_planning.a_star import AStar
from path_planning.planner import GridMapPlanner
from path_planning.maps import generate_random_obstacle_map


def _generate_random_start_end(map: np.array, max_tries=100) -> Tuple[Tuple[int, int], Tuple[int, int]]:
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

        if max_tries < attempt:
            raise Exception(
                f"Could not find start or goal in {attempt} tries. Try another map")
        attempt += 1

    return (start, goal)


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    map_rows = 100
    map_cols = 100

    gridmap = generate_random_obstacle_map(
        (map_rows, map_cols),
        obstacle="blob",
        obs_radius=15,
        obs_max=10,
        blur_sigma=2
    )
    start, goal = _generate_random_start_end(gridmap)

    print(f"A* demonstration\nMoving the robot from {start} to {goal}")
    planner = AStar()
    start_t = time.time()
    path = planner.plan(gridmap, start, goal, threshold=0.25)
    end_t = time.time()
    print("completed in {0:.2} seconds".format(end_t-start_t))

    plot = planner.plot_path(
        gridmap,
        GridMapPlanner.marshal_pose_list_for_plot(path),
        GridMapPlanner.marshal_pose_list_for_plot(planner.visited),
    )
    plt.show()
