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

# ----------------------------------------------------------------------------------------------------------------------


class Node:
    """
    We need a simple node class that defines a point on the path, it's parent and
    its cost. This is a hashable object (ie.: you can do 'in' operations with it)
    """

    def __init__(self,
                 pose: Tuple[int, int] = (0, 0),
                 cost: float = 1e9,
                 parent=None
                 ) -> None:
        self.pose = pose
        self.row = self.pose[0]
        self.col = self.pose[1]
        self.f: float = cost
        self.g: float = cost
        self.h: float = cost
        self.parent: Node = parent

    def __key(self):
        return (self.row, self.col)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.__key() == other.__key()
        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

# ----------------------------------------------------------------------------------------------------------------------
# Custom Exceptions


class OutOfBounds(Exception):
    pass


class MapError(Exception):
    pass


class NoPathError(Exception):
    pass

# ----------------------------------------------------------------------------------------------------------------------
# Helper Functions


class AStar:
    """
    This is our implementation of the A* planner
    todo:
        - abstract planner to general
        - make most ofthe helpers @classmethod statics
    """

    def __init__(self):
        self.visited: List[Tuple[int, int]] = []

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

    def _distance(self, n: Tuple[int, int], goal: Tuple[int, int]) -> float:
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

    def _movecost(self, node: Node, gridmap: np.array) -> float:
        """
        compute the movement cost into node according to gridmap
        This assumes that you are moving from a node directly adjacent to 'node' and
        that costs from all directions are symmetric
        """
        return gridmap[node[0]][node[1]]

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
        for i, n in enumerate(open):
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
        print(
            f"dbg *** the node value is {node_value}, is obs = {node_value>threshold}")
        return node_value > threshold

        # ----------------------------------------------------------------------------------------------------------------------
        # Public Methods

    def marshal_visited_for_plot(self) -> Tuple[List[int], List[int]]:
        x = []
        y = []
        for v in self.visited:
            x.append(v[1])
            y.append(v[0])

        return (x, y)

    def get_neighbors8(self, node: Node, shape: Tuple[int, int]) -> Tuple[Node]:
        """
        Gets the 8-connected neighbors of the grid point 'node'
        : param node:  the point at which to get the 8 neighbors(row, col)
        : param shape: the size of the grid map(rows, cols)
        : return: a tuple of the neighbors(row, col) in clockwise order from N to NW(inclusive)
                Neighbors that do not exist are not returned
        """
        row = node.pose[0]
        col = node.pose[1]
        neighbors = [
            Node(pose=(row-1, col)),    # North
            Node(pose=(row-1, col+1)),  # North-East
            Node(pose=(row,   col+1)),  # East
            Node(pose=(row+1, col+1)),  # South-East
            Node(pose=(row+1, col)),    # South
            Node(pose=(row+1, col-1)),  # South-West
            Node(pose=(row,   col-1)),  # West
            Node(pose=(row-1, col-1))   # North-West
        ]

        # purge all the out of bounds nodes
        true_neighbors = []
        for _, n in enumerate(neighbors):
            if n.pose[0] < 0 or n.pose[1] < 0 or shape[0] <= n.pose[0] or shape[1] <= n.pose[1]:
                continue
            else:
                true_neighbors.append(n)

        return tuple(true_neighbors)

    def get_neighbors4(self, node: Node, shape: Tuple[int, int]) -> Tuple[Node]:
        """
        Gets the 4-connected neighbors of the grid point 'node'
        : param node:  the point at which to get the 4 neighbors(row, col)
        : param shape: the size of the grid map(rows, cols)
        : return: a tuple of the neighbors(row, col) in clockwise order from N to W(inclusive)
                Neighbors that do not exist are not returned

        TODO: ROll THIS INTO THE GET_NEIGHBORS8()
        """
        row = node.pose[0]
        col = node.pose[1]
        neighbors = [
            Node(pose=(row-1, col)),    # North
            Node(pose=(row,   col+1)),  # East
            Node(pose=(row+1, col)),    # South
            Node(pose=(row,   col-1)),  # West
        ]

        # purge all the out of bounds nodes
        true_neighbors = []
        for i, n in enumerate(neighbors):
            if n.pose[0] < 0 or n.pose[1] < 0 or shape[0] <= n.pose[0] or shape[1] <= n.pose[1]:
                continue
            else:
                true_neighbors.append(n)

        return tuple(true_neighbors)

    def plan(self, gridmap: np.array, start: Tuple[int, int], goal: Tuple[int, int],
             neighbor_function: Callable[
        [Node, Tuple[int, int]],
            List[Node]] = get_neighbors8) -> List[Tuple[int, int]]:
        """
        Plans a path from 'start' to 'end' poses using the A * algorithm
        : param gridmap: the grid map matrix to plan over
        : param start:   the starting coordinates in the grid map
        : param end:     the finishing coordinates in the grid map
        : param neighbor_function: the function used to find the neighbors(defaults to 8-connected)
        : returns:       a list of all the map coordinates which comprise the best path

        todo: make own priority queue for this application
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
                self, current_node, gridmap.shape)

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
