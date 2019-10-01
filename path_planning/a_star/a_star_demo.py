#! /usr/bin/env python3
"""
Mobile Robot Path Planning: A* demonstration
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""
import numpy as np

import a_star
import maps


if __name__ == "__main__":

    map_rows = 100
    map_cols = 100

    map = maps.generate_random_obstacle_map(
        (map_rows, map_cols),
        obstacle="blob",
        obs_radius=5,
        obs_max=10,
        blur_sigma=0
    )

    start = (
        np.random.randint(low=0, high=map_rows-1),
        np.random.randint(low=0, high=map_cols-1)
    )
    goal = (
        np.random.randint(low=0, high=map_rows-1),
        np.random.randint(low=0, high=map_cols-1)
    )

    print(f"A* demonstration\nMoving the robot from {start} to {goal}")

    planner = a_star.AStar()
    path = planner.plan(map, start, goal)
    maps.plot_map(map, path=path,
                  visited=planner.marshal_visited_for_plot())
