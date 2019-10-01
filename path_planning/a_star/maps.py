#! /usr/bin/env python3
"""
Mobile Robot Path Planning: A*
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""
from typing import Tuple, Dict, List
import matplotlib.pyplot as plt

from scipy.ndimage.filters import gaussian_filter
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Private Helper Methods


def _blur_map(map: np.array, sigma=40) -> np.array:
    """
    fuzzify the edges of the obstacles to make the map non-binary
    :param map: the numpy matrix representing the binary map
    :return: the blured map (this is also an in place operation)
    """
    return gaussian_filter(map, sigma=sigma)


def _get_obstacle_centers(map: np.array, obs_max: int) -> List[Tuple[int, int]]:
    """
    :return: obs_max random obstacle centers of form (row, col) in map
    """
    centers = []
    row_count, col_count = map.shape

    for _ in range(0, obs_max):
        centers.append(
            (np.random.randint(0, row_count),
             np.random.randint(0, col_count))
        )
    return centers


def _paint_circle(map: np.array, center: Tuple[int, int], r: int) -> None:
    """
    Simple algorithm to paint a circle at center in map. This very crudely
    walks through all the pixels in the circle's bounding box, giving a
    completion time of O(r^2)
    """
    row_count, col_count = map.shape

    x_min = center[0] - r if center[0] - r > 0 else 0
    x_max = center[0] + r if center[0] + r < col_count else col_count-1
    #
    y_min = center[1] - r if center[1] - r > 0 else 0
    y_max = center[1] + r if center[1] + r < row_count else row_count-1

    for row in range(y_min, y_max):
        for col in range(x_min, x_max):
            dx = center[0] - col
            dy = center[1] - row
            if (dx**2 + dy**2) < r**2:
                map[row][col] = 1.0


def _create_blob_obstacles(map: np.array, obs_max: int, obs_radius: float) -> np.array:
    """
    create circular blob obstacles
    """
    centers = _get_obstacle_centers(map, obs_max)
    for c in centers:
        rad = int(round(np.random.uniform(low=-0.25, high=0.25) * obs_radius))
        _paint_circle(map, c, rad)

    return map


def _create_rect_obstacles(map: np.array, obs_max: int, obs_radius: float) -> np.array:
    """
    create rectangular obstacles
    """
    raise Exception("Have not implemented create_rect_obstacles!")
    return map


def _marshal_path_for_plot(path: List[Tuple[int, int]]) -> Tuple[List[int], List[int]]:
    """
    Re-arranges the path pairs into x and y lists
    """
    x = []
    y = []
    for p in path:
        x.append(p[0])
        y.append(p[1])

    return (x, y)

# ----------------------------------------------------------------------------------------------------------------------
# Public Map Generation and Plotting Methods


def generate_random_obstacle_map(
        size: Tuple[int, int],
        obstacle: str = "blob",
        obs_max: int = 10,
        obs_radius: float = 10) -> np.array:
    """
    creates a grid map of obstacles and clear space to a defined size
    :param size:       the (x,y) dimensions of the map
    :param obstacle:   the style of the obstacles, can be [blob, ]
    :param obs_max:    the number of obstacles to seed (these may flow into each other)
    :param obs_radius: the rough radius of obstacles (this is a basis of random variance)
    returns: a map with random obstacles of size 'size'
    """
    map = np.zeros(size, dtype=float)

    if obstacle == "blob":
        map = _create_blob_obstacles(map, obs_max, obs_radius)

    elif obstacle == "rect":
        map = _create_rect_obstacles(map, obs_max, obs_radius)

    else:
        raise Exception(f"obstacle type {obstacle} is unknown")

    return _blur_map(map)


def plot_map(map: np.array, path: List[Tuple[int, int]] = None, scale=1.0) -> None:
    """
    Use Matplotlib to plot the obstacle map and the path
    :param map:   the 2D obstacle map
    :param path:  the 2D path through the map
    :param scale: scaling factor for the map and path TODO: IMPLEMENT
    """
    fig = plt.figure()
    plt.title("Obstacle Map and Path", fontsize=20)
    plt.xlabel("X", fontsize=15)
    plt.ylabel("Y", fontsize=15)

    # plot the map
    plt.imshow(map, cmap="bone_r")

    # plot the path
    if path:
        path_x, path_y = _marshal_path_for_plot(path)

        plt.plot(path_x, path_y,
                 color="DodgerBlue",
                 label="Robot Path")

        plt.plot(path_x[0], path_y[0],
                 color="DodgerBlue",
                 marker='o',
                 markersize=8,
                 label="Start Point")
        plt.plot(path_x[-1], path_y[-1],
                 color="DodgerBlue",
                 marker='d',
                 markersize=8,
                 label="Goal Point")

    plt.legend(fontsize=15)
    plt.grid()
    plt.show()


# ----------------------------------------------------------------------------------------------------------------------
# TESTING
if __name__ == "__main__":
    map = generate_random_obstacle_map(
        (1000, 1000), obstacle="blob", obs_radius=500, obs_max=40)

    plot_map(map, path=[(100, 100), (400, 400)])
