#! /usr/bin/env python3
"""
Mobile Robot Path Planning: A*
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""
from typing import Tuple, Dict, List, Callable
import matplotlib.pyplot as plt
import numpy as np

from path_planning.pqueue import Pqueue
from path_planning.planner import Node, GridMapPlanner, OutOfBoundsError, MapError, NoPathError

# ----------------------------------------------------------------------------------------------------------------------
# Helper Functions


class AStar(GridMapPlanner):
    """
    This is our implementation of the A* planner
    """

    def __init__(self):
        super().__init__()

    # ----------------------------------------------------------------------------------------------------------------------
    # Public Methods

    def plan(self,
             gridmap: np.array,
             start: Tuple[int, int],
             goal: Tuple[int, int],
             threshold: float = 1.0,
             neighbor_function: Callable[
                 [Node, Tuple[int, int]], List[Node]] = GridMapPlanner.get_neighbors) -> List[Tuple[int, int]]:
        """
        Plans a path from 'start' to 'end' poses using the A * algorithm
        """

        GridMapPlanner.sanity_check_map(gridmap)
        GridMapPlanner.sanity_check_point(gridmap, start)
        GridMapPlanner.sanity_check_point(gridmap, goal)

        open = Pqueue()
        open.insert(
            # the starting node has 0 cost
            (0.0, Node(pose=start, cost=0.0, parent=None))
        )
        closed = set()

        # convert the start, goal to a node for comparison
        start_node = Node(pose=start)
        goal_node = Node(pose=goal)

        # perform the A* search for a path...
        while open.size():

            current_node = open.pop(goal)
            closed.add(current_node)

            # check goal arrival
            if current_node == goal_node:
                return GridMapPlanner.reconstruct_path(current_node)

            neighbor_nodes = neighbor_function(
                current_node, gridmap.shape, connected=8)

            for n in neighbor_nodes:
                self.visited.append(n.pose)  # for plotting

                if n in closed or GridMapPlanner.is_obstacle(gridmap, n.pose, threshold=threshold):
                    closed.add(n)
                    continue

                g_n = self._g(current_node, start_node)

                if not open.contains(n):
                    n.parent = current_node
                    n.g = g_n
                    n.h = self._h(n, goal_node)
                    n.f = n.g + n.h
                    open.insert((n.f, n))

                else:
                    if g_n < n.g:
                        n.g = g_n
                        n.f = n.g + n.h
                        n.parent = current_node
                        open.resort()

        raise NoPathError

    def plot_path(self,
                  gridmap: np.array,
                  path: Tuple[List[int], List[int]],
                  visited: Tuple[List[int], List[int]]) -> plt.Figure:
        """
        Use Matplotlib to plot the obstacle map and the path
        :param map:   the 2D obstacle map
        :param path:  the 2D path through the map (row, col in grid map)
        :param scale: scaling factor for the map and path TODO: IMPLEMENT
        :param visited: a tuple containing the x and y coordinates of the visited nodes
        """
        fig = plt.figure(figsize=(15, 10))
        plt.title("Obstacle Map and Path (A* Planner)", fontsize=18)
        plt.xlabel("X (units)", fontsize=15)
        plt.ylabel("Y (units)", fontsize=15)

        # plot the map
        plt.imshow(gridmap, cmap="bone_r")

        # plot all the visited nodes
        plt.plot(visited[1], visited[0],
                 color="Peru",
                 marker='o',
                 alpha=0.1,
                 linewidth=0.0,
                 markeredgewidth=0.0,
                 markersize=5,
                 label="Visited Node")

        # plot the path
        plt.plot(path[1], path[0],
                 color="Red",
                 label="Robot Path")

        # plot the start point
        plt.plot(path[1][0], path[0][0],
                 color="OrangeRed",
                 marker='o',
                 markersize=6,
                 linewidth=0,
                 markeredgecolor="Black",
                 markeredgewidth=0.5,
                 label="Start Point")

        # plot the end point
        plt.plot(path[1][-1], path[0][-1],
                 color="OrangeRed",
                 marker='*',
                 linewidth=0,
                 markersize=10,
                 markeredgecolor="Black",
                 markeredgewidth=0.5,
                 label="Goal Point")

        # plot empty 'obstacle' for legend
        plt.plot([], [],
                 color='k', marker='s', markersize=5, linewidth=0, label="Obstacle")

        plt.legend(bbox_to_anchor=(1.25, 1), fontsize=10, loc='upper right')
        plt.grid()

        return fig

    # ------------------------------------------------------------------------------------------------------------------

    def _g(self, current_node: Node, start_node: Node) -> float:
        """
        The cost from the starting node to n
        """

        if current_node.parent:
            return current_node.parent.g + current_node.distance(current_node.parent)
        else:
            return 0.0

    def _h(self, n: Node, goal: Node) -> float:
        """
        This is the cost from node 'n' to 'goal', the _heuristic_ for this pose
        At this time we use the linear distance
        : param n:    the node we are computing position from
        : param goal: the node we are computing position to
        : return:     the heuristic for n to goal
        """
        return n.distance(goal)
