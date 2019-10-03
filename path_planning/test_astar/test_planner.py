#! /usr/bin/env python3
"""
Mobile Robot Path Planning: Base Planner Testing
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""

import unittest
import numpy as np
from path_planning.planner import Node, GridMapPlanner


class TestNode(unittest.TestCase):

    def test_eq(self):
        n1 = Node(pose=(0, 0))
        self.assertTrue(n1 == Node(pose=(0, 0)))
        self.assertFalse(n1 == Node(pose=(0, 1)))

    def test_in(self):
        n1 = Node(pose=(0, 0))
        nodes = [
            Node(pose=(0, 0)),
            Node(pose=(0, 1)),
            Node(pose=(0, 2))
        ]
        self.assertTrue(n1 in nodes)
        self.assertTrue(Node(pose=(0, 0)) in nodes)

        n2 = Node(pose=(1, 1))
        self.assertFalse(n2 in nodes)

    def test_less_than(self):
        n1 = Node()
        n1.f = 1234.5678
        n2 = Node()
        n2.f = 0.0

        self.assertTrue(n1 > n2)
        self.assertFalse(n1 < n2)

    def test_distance(self):
        n1 = Node(pose=(0, 0))
        n2 = Node(pose=(5, 5))
        expected = np.sqrt(5*5 + 5*5)
        actual = n1.distance(n2)
        self.assertAlmostEqual(expected, actual)

# ----------------------------------------------------------------------------------------------------------------------


class TestGridMapPlanner(unittest.TestCase):

    def test_is_obstacle(self):
        rows = 5
        cols = 5
        a1 = np.ones((rows, cols))
        a2 = np.zeros((rows, cols))

        for r in range(0, rows):
            for c in range(0, cols):
                self.assertTrue(GridMapPlanner.is_obstacle(
                    a1, (r, c), threshold=0.5))
                self.assertFalse(GridMapPlanner.is_obstacle(
                    a2, (r, c), threshold=0.5))

    def test_get_neighbors_8(self):

        rows = 10
        cols = 10
        grid = np.zeros((rows, cols))

        r2 = int(rows/2.0)
        c2 = int(cols/2.0)

        # dict of pose (key) and neighbors expected (value)
        poses = {
            (0, 0): [(0, 1), (1, 0), (1, 1)],
            (rows-1, cols-1): [(rows-2, cols-2), (rows-2, cols-1), (rows-1, cols-2)],
            (r2, c2):
                [(r2-1, c2),    # N
                 (r2-1, c2+1),  # NE
                 (r2,   c2+1),  # E
                 (r2+1, c2+1),  # SE
                 (r2+1, c2),    # S
                 (r2+1, c2-1),  # SW
                 (r2,   c2-1),  # W
                 (r2-1, c2-1)]  # NW
        }

        for p in poses:
            neighbors = GridMapPlanner.get_neighbors(
                Node(pose=p), grid.shape, connected=8)

            # check the correct number of poses was returned
            self.assertEqual(len(neighbors), len(poses[p]))

            # check the returned poses was as expected
            for n in neighbors:
                self.assertTrue(n.pose in poses[p])

    def test_get_neighbors_4(self):

        rows = 10
        cols = 10
        grid = np.zeros((rows, cols))

        r2 = int(rows/2.0)
        c2 = int(cols/2.0)

        # dict of pose (key) and neighbors expected (value)
        poses = {
            (0, 0): [(0, 1), (1, 0)],
            (rows-1, cols-1): [(rows-2, cols-1), (rows-1, cols-2)],
            (r2, c2):
                [(r2-1, c2),    # N
                 (r2,   c2+1),  # E
                 (r2+1, c2),    # S
                 (r2,   c2-1)]  # W
        }

        for p in poses:
            neighbors = GridMapPlanner.get_neighbors(
                Node(pose=p), grid.shape, connected=4)

            # check the correct number of poses was returned
            self.assertEqual(len(neighbors), len(poses[p]))

            # check the returned poses was as expected
            for n in neighbors:
                self.assertTrue(n.pose in poses[p])


if __name__ == "__main__":
    unittest.main()
