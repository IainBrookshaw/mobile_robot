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

from pqueue import Pqueue
from planner import Node, GridMapPlanner, OutOfBoundsError, MapError, NoPathError

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
             neighbor_function: Callable[
                 [Node, Tuple[int, int]], List[Node]] = GridMapPlanner.get_neighbors) -> List[Tuple[int, int]]:
        """
        Plans a path from 'start' to 'end' poses using the A * algorithm
        """

        self._sanity_check_map(gridmap)
        self._sanity_check_start_and_end(gridmap, start, goal)

        open = Pqueue()
        open.insert(
            # the starting node has 0 cost
            (0.0, Node(pose=start, cost=0.0, parent=None))
        )
        closed = set()

        # convert the goal to a node for comparison
        goal_node = Node(pose=goal)

        # perform the A* search for a path...
        while open.size():

            current_node = open.pop()
            closed.add(current_node)

            # check goal arrival
            if current_node == goal_node:
                self._save_closed(closed)  # TODO: This is really clunky
                return self._reconstruct_path(current_node)

            neighbor_nodes = neighbor_function(
                current_node, gridmap.shape, connected=8)

            for n in neighbor_nodes:

                if n in closed or self._is_obstacle(n, gridmap):
                    continue

                if not open.contains(n):
                    n.parent = current_node
                    n.g = self._g(n)
                    n.h = self._h(n.pose, goal_node.pose)
                    n.f = n.g + n.h
                    open.insert((n.f, n))

                else:
                    if self._g(n) < n.g:
                        n.g = self._g(n)
                        n.f = n.g + n.h
                        n.parent = current_node
                        open.resort()

        raise NoPathError

    def plot_path(self, gridmap: np.array,
                  path: Tuple[List[int], List[int]],
                  visited: Tuple[List[int], List[int]]) -> plt.Figure:
        """
        Use Matplotlib to plot the obstacle map and the path
        :param map:   the 2D obstacle map
        :param path:  the 2D path through the map (row, col in grid map)
        :param scale: scaling factor for the map and path TODO: IMPLEMENT
        :param visited: a tuple containing the x and y coordinates of the visited nodes
        """
        fig = plt.figure()
        plt.title("Obstacle Map and Path (A* Planner)", fontsize=18)
        plt.xlabel("X (units)", fontsize=15)
        plt.ylabel("Y (units)", fontsize=15)

        # plot the map
        plt.imshow(gridmap, cmap="bone_r")

        # plot the path
        plt.plot(path[1], path[0],
                 color="Salmon",
                 label="Robot Path")

        # plot the start and end points
        plt.plot(path[1][0], path[1][0],
                 color="OrangeRed",
                 marker='o',
                 markersize=5,
                 linewidth=0,
                 label="Start Point")
        plt.plot(path[1][-1], path[0][-1],
                 color="OrangeRed",
                 marker='*',
                 linewidth=0,
                 markersize=9,
                 label="Goal Point")

        # plot all the visited nodes
        for i in range(0, len(visited[0])):
            plt.plot(visited[0][i], visited[1][i],
                     color="Peru",
                     marker='o',
                     alpha=0.1,
                     markeredgewidth=0.0,
                     markersize=5)

        # plot some empties so that obstacles and visited nodes will show in the legend
        plt.plot([], [],
                 color="Peru", marker='o', markersize=5, linewidth=0, label="Visited Points")
        plt.plot([], [],
                 color='k', marker='s', markersize=5, linewidth=0, label="Obstacle")

        plt.legend(bbox_to_anchor=(1, 0), fontsize=10, loc='upper right')
        plt.grid()

        return fig

    # ------------------------------------------------------------------------------------------------------------------

    def _marshal_path_for_plot(self, path: List[Tuple[int, int]]) -> Tuple[List[int], List[int]]:
        """
        Re-arranges the path pairs into x and y lists
        """
        x = []
        y = []
        for p in path:
            x.append(p[1])
            y.append(p[0])

        return (x, y)

    def _g(self, n: Node) -> float:
        return 0.0  # TODO: Implement

    def _h(self, n: Tuple[int, int], goal: Tuple[int, int]) -> float:
        """
        This is the cost from node 'n' to 'goal', the _heuristic_ for this pose
        At this time we use the linear distance
        : param n:    the node we are computing position from (row, col)
        : param goal: the node we are computing position to(row, col)
        : return:     the heuristic for n to goal
        """
        d_row = goal[0] - n[0]
        d_col = goal[1] - n[1]
        return np.sqrt(d_row**2 + d_col**2)

    def _sanity_check_map(self, gridmap: np.array) -> None:
        if gridmap.shape[0] < 2 or gridmap.shape[1] < 2:
            raise MapError()

    def _sanity_check_start_and_end(self, gridmap: np.array, start: Tuple[int, int], end: Tuple[int, int]) -> None:

        rows, cols = gridmap.shape

        if start[0] < 0 or start[1] < 0 or rows <= start[0] or cols <= start[1]:
            raise OutOfBoundsError(
                f"starting pose {start} is out of map bounds {gridmap.shape}")

        if end[0] < 0 or end[1] < 0 or rows <= end[0] or cols <= end[1]:
            raise OutOfBoundsError(
                f"ending pose {end} is out of map bounds {gridmap.shape}")

    def _is_node_in_open(self, node: Node, open: List[Tuple[float, Node]]) -> bool:
        """
        checks to see if 'node' in 'open' queue without changing the queue's state
        """
        for x in open:
            if node == x[1]:
                return True

        return False

    def _remove_from_open(self, node: Node, open: List[Tuple[float, Node]]) -> None:
        for i, _ in enumerate(open):
            open = open[:i] + open[i+1:]

    def _reconstruct_path(self, end_node: Node) -> List[Tuple[int, int]]:
        """
        builds the path from the connected nodes. Raises exception if the nodes
        broken
        """
        path = [end_node.pose]
        node = end_node
        while node.parent is not None:
            path.append(node.pose)
            node = node.parent

        path.reverse()
        return path

    def _save_closed(self, closed_set) -> None:
        for node in closed_set:
            self.visited.append(node.pose)

    def _is_obstacle(self, node: Node, gridmap: np.array, threshold=0):
        node_value = gridmap[node.pose[0]][node.pose[1]]
        return node_value > threshold
