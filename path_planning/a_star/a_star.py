#! /usr/bin/env python3
"""
Mobile Robot Path Planning: A*
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""
from typing import Tuple, Dict, List
import numpy as np
import queue


class Node:
    """
    We need a simple node class that defines a point on the path, it's parent and 
    its cost
    """

    def __init__(self,
                 pose: Tuple(int, int) = (0, 0),
                 cost: float = 0.0,
                 parent: Node = None
                 ) -> None:
        self.pose: Tuple(int, int) = pose
        self.cost: float = cost
        self.parent: Node = parent


class OutOfBounds(Exception):
    pass


class MapError(Exception):
    pass

# ----------------------------------------------------------------------------------------------------------------------
# Helper Functions


def _g(n: Node) -> float:
    return 0.0  # TODO: Implement


def _h(n: Node) -> float:
    return 0.0  # TODO: Implement


def _movecost(start: Node, end: Node) -> float:
    return 0.0  # TODO: Implement


def _sanity_check_map(gridmap) -> None:
    pass  # Todo: Implement


def _sanity_check_start_and_end(gridmap, start: Tuple[int, int], end: Tuple[int, int]) -> None:
    pass  # Todo: Implement


def plan(gridmap, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Plans a path from 'start' to 'end' poses using the A* algorithm
    :param gridmap: the grid map matrix to plan over
    :param start:   the starting coordinates in the grid map
    :param end:     the finishing coordinates in the grid map
    :returns:       a list of all the map coordinates which comprise the best path

    TODO:
    - 
    """

    _sanity_check_map(gridmap)
    _sanity_check_start_and_end(gridmap, start, end)

    open = queue.PriorityQueue()
    open.add(Node(pose=start, cost=0.0, parent=None))

    closed = set()

    while _get_lowest_rank(open) is not end:

        current = _pop_lowest_rank(open)
        closed.add(current)

        for n in _get_neighbors(gridmap, current):

            cost = _g(current) + _movecost(current, n)

            if n in open and cost < _g(n):
                open.remove(n)

            if n in closed and cost < _g(n):
                closed.remove(n)

            if n not in open and n not in closed:
                n.cost = _g(n) + _h(n)
                n.parent = current
                open.put((n.cost, n))

    # We now have the path (if one exists!) and can marshal it for return
    path = []
    n = _get_lowest_rank(open)
    while n.parent:
        path.append(n.pose)
        n = n.parent

    return reverse(path)
