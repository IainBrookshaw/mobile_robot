#! /usr/bin/env python3
"""
Mobile Robot Path Planning: A* demonstration
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""
from typing import Tuple
import numpy as np
import a_star
import maps


def _generate_random_start(map: np.array) -> Tuple[Tuple[int, int], Tuple[int, int]]:

    map_rows = map.shape[0]
    map_cols = map.shape[1]

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

    return (start, goal)


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    map_rows = 100
    map_cols = 100

    map = maps.generate_random_obstacle_map(
        (map_rows, map_cols),
        obstacle="blob",
        obs_radius=10,
        obs_max=8,
        blur_sigma=0
    )
    start, goal = _generate_random_start(map)

    print(f"A* demonstration\nMoving the robot from {start} to {goal}")
    planner = a_star.AStar()
    path = planner.plan(map, start, goal)
    maps.plot_map(map, path=path,
                  visited=planner.marshal_visited_for_plot())
