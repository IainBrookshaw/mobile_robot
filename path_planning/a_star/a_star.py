#! /usr/bin/env python3
"""
Mobile Robot Path Planning: A*
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""
from typing import Tuple, Dict, List, Callable
import numpy as np
import queue

# ----------------------------------------------------------------------------------------------------------------------


class Node:
    """
    We need a simple node class that defines a point on the path, it's parent and
    its cost. This is a hashable object (ie.: you can do 'in' operations with it)
    """

    def __init__(self,
                 pose: Tuple[int, int] = (0, 0),
                 cost: float = 0.0,
                 parent=None
                 ) -> None:
        self.pose = pose
        self.row = self.pose[0]
        self.col = self.pose[1]
        self.cost: float = cost
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
        return self.cost < other.cost

    def __gt__(self, other):
        return self.cost > other.cost


class OutOfBounds(Exception):
    pass


class MapError(Exception):
    pass

# ----------------------------------------------------------------------------------------------------------------------
# Helper Functions


def _g(n: Node) -> float:
    return 0.0  # TODO: Implement


def _h(n: Tuple[int, int], goal: Tuple[int, int]) -> float:
    """
    This is the cost from node 'n' to 'goal', the _heuristic_ for this pose
    At this time we use the linear distance
    :param n:    the node we are computing position from (row, col)
    :param goal: the node we are computing position to (row, col)
    :return:     the heuristic for n to goal
    """
    d_row = goal[0] - n[0]
    d_col = goal[1] - n[1]
    return np.sqrt(d_row**2 + d_col**2)


def _movecost(node: Node, gridmap: np.array) -> float:
    """
    compute the movement cost into node according to gridmap
    This assumes that you are moving from a node directly adjacent to 'node' and
    that costs from all directions are symmetric
    """
    return gridmap[node[0]][node[1]]


def _sanity_check_map(gridmap: np.array) -> None:
    if gridmap.shape[0] < 2 or gridmap.shape[1] < 2:
        raise MapError()


def _sanity_check_start_and_end(gridmap: np.array, start: Tuple[int, int], end: Tuple[int, int]) -> None:

    rows, cols = gridmap.shape

    if start[0] < 0 or start[1] < 0 or rows <= start[0] or cols <= start[1]:
        raise OutOfBounds(
            f"starting pose {start} is out of map bounds {gridmap.shape}")

    if end[0] < 0 or end[1] < 0 or rows <= end[0] or cols <= end[1]:
        raise OutOfBounds(
            f"ending pose {end} is out of map bounds {gridmap.shape}")


def _is_node_in_open(node: Node, open: List[Tuple[float, Node]]) -> bool:
    """
    checks to see if 'node' in 'open' queue without changing the queue's state
    """
    for x in open:
        if node == x[1]:
            return True

    return False


def _remove_from_open(node: Node, open: List[Tuple[float, Node]]) -> None:
    for i, n in enumerate(open):
        open = open[:i] + open[i+1:]

# ----------------------------------------------------------------------------------------------------------------------
# Public Methods


def get_neighbors8(node: Node, shape: Tuple[int, int]) -> Tuple[Node]:
    """
    Gets the 8-connected neighbors of the grid point 'node'
    :param node:  the point at which to get the 8 neighbors (row, col)
    :param shape: the size of the grid map (rows, cols)
    :return: a tuple of the neighbors (row,col) in clockwise order from N to NW (inclusive)
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
    for i, n in enumerate(neighbors):
        if n.pose[0] < 0 or n.pose[1] < 0 or shape[0] <= n.pose[0] or shape[1] <= n.pose[1]:
            continue
        else:
            true_neighbors.append(n)

    return tuple(true_neighbors)


def get_neighbors4(node: Node, shape: Tuple[int, int]) -> Tuple[Node]:
    """
    Gets the 4-connected neighbors of the grid point 'node'
    :param node:  the point at which to get the 4 neighbors (row, col)
    :param shape: the size of the grid map (rows, cols)
    :return: a tuple of the neighbors (row,col) in clockwise order from N to W (inclusive)
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


def plan(gridmap: np.array, start: Tuple[int, int], goal: Tuple[int, int],
         neighbor_function: Callable[
             [Node, Tuple[int, int]],
             List[Node]] = get_neighbors8) -> List[Tuple[int, int]]:
    """
    Plans a path from 'start' to 'end' poses using the A * algorithm
    :param gridmap: the grid map matrix to plan over
    :param start:   the starting coordinates in the grid map
    :param end:     the finishing coordinates in the grid map
    :param neighbor_function: the function used to find the neighbors (defaults to 8-connected)
    : returns:       a list of all the map coordinates which comprise the best path

    TODO:
    -
    """

    _sanity_check_map(gridmap)
    _sanity_check_start_and_end(gridmap, start, goal)

    open = [
        (0.0, Node(pose=start, cost=0.0, parent=None))  # the starting node
    ]
    running_cost = 0.0
    closed = set()

    # convert the goal to a node for comparison
    goal = Node(pose=goal)

    # perform the A* search for a path...
    while True:

        # get the next node and check for arrival
        if not len(open):
            raise Exception("there are no more open nodes to explore!")
        else:
            open.sort()

        current = open[0][1]
        if current is goal:
            break

        print(f"dbg *** current = {current.pose}")

        # look at all the neighbors of current
        for n in neighbor_function(current, gridmap.shape):
            print(f"\tneighbor = {n.pose}")

            # compute g(n), the exact cost, from start to the neighbor 'n'
            g_n = running_cost + _movecost(n.pose, gridmap)

            # compute the heuristic from n to goal
            h_n = _h(n.pose, goal.pose)

            # the cost of node 'n' is thus:
            f_n = g_n + h_n

            # if this neighbor node is in open, but the cost is lower, remove n from open
            if _is_node_in_open(n, open) and f_n < n.cost:
                _remove_from_open(n, open)

            # if n is closed, but new cost is lower, reopen n for consideration
            # this really shouldn't happen
            if n in closed and f_n < n.cost:
                closed.remove(n)

            if not _is_node_in_open(n, open) and n not in closed:

                n.cost = f_n
                n.parent = current
                open.append(
                    (n.cost, n)
                )

    # We now have the path (if one exists!) and can marshal it for return
    path = []
    n = open.pop()
    while n.parent:
        path.append(n.pose)
        n = n.parent

    return path.reverse()
