#! /usr/bin/env python3
"""
Mobile Robot Path Planning: A*
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""
from typing import Tuple, Dict, List, Callable
import numpy as np
# import queue
from pqueue import Pqueue
from planner import Node, GridMapPlanner

# ----------------------------------------------------------------------------------------------------------------------
# Custom Exceptions


class OutOfBounds(Exception):
    """Exception for leaving the gridmap"""
    pass


class MapError(Exception):
    """Exception for problems with the map"""
    pass


class NoPathError(Exception):
    """Exception for no possible path from start to goal, run out of map to search"""
    pass

# ----------------------------------------------------------------------------------------------------------------------
# Helper Functions


class AStar(GridMapPlanner):
    """
    This is our implementation of the A* planner
    todo:
        - abstract planner to general
        - make most ofthe helpers @classmethod statics
    """

    def __init__(self):
        self.visited: List[Tuple[int, int]] = []
    # ----------------------------------------------------------------------------------------------------------------------
        # Public Methods

    def marshal_visited_for_plot(self) -> Tuple[List[int], List[int]]:
        x = []
        y = []
        for v in self.visited:
            x.append(v[1])
            y.append(v[0])

        return (x, y)

    def plan(self,
             gridmap: np.array,
             start: Tuple[int, int],
             goal: Tuple[int, int],
             neighbor_function: Callable[
                 [Node, Tuple[int, int]],
            List[Node]] = GridMapPlanner.get_neighbors8) -> List[Tuple[int, int]]:
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
                current_node, gridmap.shape)

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

        raise NoPathError()

    # ------------------------------------------------------------------------------------------------------------------

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
            raise OutOfBounds(
                f"starting pose {start} is out of map bounds {gridmap.shape}")

        if end[0] < 0 or end[1] < 0 or rows <= end[0] or cols <= end[1]:
            raise OutOfBounds(
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
