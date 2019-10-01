#! /usr/bin/env python3
"""
Mobile Robot Path Planning: A* demonstration
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""
import a_star
import maps


if __name__ == "__main__":

    map_rows = 100
    map_cols = 100

    map = maps.generate_random_obstacle_map(
        (map_rows, map_cols),
        obs_radius=20
    )

    start = (0, 0)
    goal = (map_rows, map_cols)

    path = a_star.plan(map, start, goal)
    maps.plot_map(map, path=path)
