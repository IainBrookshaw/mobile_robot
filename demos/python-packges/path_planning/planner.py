#! /usr/bin/env python3
"""
Mobile Robot Path Planning: Abstract Planner
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""
from typing import Tuple, Dict, List, Callable
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Custom Exceptions


class OutOfBoundsError(Exception):
    """Exception for leaving the gridmap"""
    pass


class MapError(Exception):
    """Exception for problems with the map"""
    pass


class NoPathError(Exception):
    """Exception for no possible path from start to goal, run out of map to search"""
    pass

# ----------------------------------------------------------------------------------------------------------------------


class Node:
    """
    We need a simple node class that defines a point on the path, it's parent and
    its costs. This is a hashable object (ie.: you can do 'in' operations with it)
    """

    def __init__(self,
                 pose: Tuple[int, int] = (0, 0),
                 cost: float = 1e9,
                 parent=None
                 ) -> None:
        self.pose = pose
        self.row = self.pose[0]
        self.col = self.pose[1]
        self.f: float = cost  # total cost (f(n) = g(n) + h(n) for A*)
        self.g: float = 0     # position cost (to start)
        self.h: float = None  # heuristic cost (to end)
        self.parent: Node = parent

    def distance2(self, n2) -> float:
        """compute the square of the euclidian distance between nodes"""
        d_row = self.pose[0] - n2.pose[0]
        d_col = self.pose[1] - n2.pose[1]
        return d_row*d_row + d_col*d_col

    def distance(self, n2) -> float:
        """compute the euclidian distance between nodes"""
        return np.sqrt(self.distance2(n2))

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


class GridMapPlanner:
    """
    This is the base abstract class for planning a path from 'start' to 'goal'
    through a rectilinear gridmap
    """

    def __init__(self):
        self.visited = []
        self.path = []

    def plan(self,
             gridmap: np.array,
             start: Tuple[int, int],
             goal: Tuple[int, int],
             threshold: float = 1.0,
             neighbor_function: Callable[[
                 Node, Tuple[int, int]], List[Node]] = None
             ) -> List[Tuple[int, int]]:
        """
        : param gridmap:           the grid map matrix to plan over
        : param start:             the starting coordinates in the grid map
        : param end:               the finishing coordinates in the grid map
        : param threshold:         the obstacle threshold [0,1]
        : param neighbor_function: the function used to find the neighbors(defaults to 8-connected)
        : returns:                 a list of all the map coordinates which comprise the best path
        """

        raise NotImplementedError

    def plot_path(self, gridmap: np.array,
                  path: Tuple[List[int], List[int]],
                  visited: Tuple[List[int], List[int]]) -> plt.Figure:
        """
        :param gridmap: the 2d world map
        :param path:    the tuple of [row, col] points in the map that form the path. First entry is [start], last entry is [goal]
        :param visited: the tuple of [row, col] points in the map that were considered by this
        :return: the matplotlib figure. This method does _not_ call the plt.show() method, as planners may require custom plots
        """
        raise NotImplementedError

    def add_node_as_visited(self, node: Node):
        """
        flag this node as visited for plotting purposes. This is for recording and has no effect on the planner
        """
        self.visited.append(node.pose)

    @classmethod
    def reconstruct_path(cls, end_node: Node, start_pose: Tuple[int, int] = None) -> List[Tuple[int, int]]:
        """
        builds the path from the connected nodes. Raises exception if the nodes
        broken
        :param end_node:   the last point (goal) of the path, this will provide a link back to it's parent
        :param start_pose: optional, add a start pose to check that the path is complete
        :return: the path as a list of [row, col] tuples in order from start to end
        """
        path = [end_node.pose]
        node = end_node
        while node.parent is not None:
            node = node.parent
            path.append(node.pose)

        path.reverse()

        # check that we got back to the start
        if start_pose and path[0] != start_pose:
            raise NoPathError

        return path

    @classmethod
    def is_obstacle(cls, gridmap: np.array, point: Tuple[int, int], threshold=0.0) -> bool:
        """
        checks to see if this gridpoint is an obstacle (as defined by threshold)
        :param gridmap:   the map object
        :param point:     the [row,col] tuple we are checking
        :param threshold: the definition of the obstacle->clear-space transition
        :return: is_obstacle ?
        """
        node_value = gridmap[point[0]][point[1]]
        return threshold < node_value

    @classmethod
    def sanity_check_map(cls, gridmap: np.array) -> None:
        """Is this healthy gridmap? raise an error if not"""
        if gridmap.shape[0] < 2 or gridmap.shape[1] < 2:
            raise MapError()

    @classmethod
    def sanity_check_point(cls, gridmap: np.array, point: Tuple[int, int]) -> None:
        """
        checks to make sure 'point' is inside the gridmap, raises OutOfBoundsError if not
        : param gridmap: the map to plan over
        : param point:   the point to check in [row, col] order
        """
        rows, cols = gridmap.shape
        if point[0] < 0 or point[1] < 0 or rows <= point[0] or cols <= point[1]:
            raise OutOfBoundsError(
                f"point {point} is out of map bounds {gridmap.shape}")

    @classmethod
    def marshal_pose_list_for_plot(cls, pose_list: List[Tuple[int, int]]) -> Tuple[List[int], List[int]]:
        """
        This system stores posers as lists of(row, col) tuples. These are difficult to plot using matplotlib
        Here any such list can be converted into a tuple of(row, col) lists
        : param pose_list: the list of tuples to convert
        : return: a tuple of two lists for plotting
        """
        x, y = [], []
        for v in pose_list:
            x.append(v[1])
            y.append(v[0])

        return (y, x)

    @classmethod
    def get_neighbors(cls, node: Node, shape: Tuple[int, int], connected: int = 8) -> Tuple[Node]:
        """
        Gets the 8-connected neighbors of the grid point 'node'
        : param node:      the point at which to get the 8 neighbors(row, col)
        : param shape:     the size of the grid map(rows, cols)
        : param connected: connectivity of the neighbors(eg: 4, 8, etc.)
        : return: a tuple of the neighbors(row, col) in clockwise order from N to NW(inclusive)
                Neighbors that do not exist are not returned
        """
        row = node.pose[0]
        col = node.pose[1]

        if connected == 8:
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

        elif connected == 4:
            neighbors = [
                Node(pose=(row-1, col)),    # North
                Node(pose=(row,   col+1)),  # East
                Node(pose=(row+1, col)),    # South
                Node(pose=(row,   col-1)),  # West
            ]
        else:
            raise Exception(
                "only 4 and 8 neighbor connectivity supported at this time")

        # purge all the out of bounds nodes
        true_neighbors = []
        for _, n in enumerate(neighbors):
            if n.pose[0] < 0 or n.pose[1] < 0 or shape[0] <= n.pose[0] or shape[1] <= n.pose[1]:
                continue
            else:
                true_neighbors.append(n)

        return tuple(true_neighbors)
