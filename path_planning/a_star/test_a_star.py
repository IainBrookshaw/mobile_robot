#! /usr/bin/env python3
"""
Mobile Robot Path Planning: A* Testing
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""

import unittest
import numpy as np

import a_star


class TestNode(unittest.TestCase):

    def test_eq(self):
        n1 = a_star.Node(pose=(0, 0))
        self.assertTrue(n1 == a_star.Node(pose=(0, 0)))
        self.assertFalse(n1 == a_star.Node(pose=(0, 1)))

    def test_in(self):
        n1 = a_star.Node(pose=(0, 0))
        nodes = [
            a_star.Node(pose=(0, 0)),
            a_star.Node(pose=(0, 1)),
            a_star.Node(pose=(0, 2))
        ]
        self.assertTrue(n1 in nodes)
        self.assertTrue(a_star.Node(pose=(0, 0)) in nodes)

        n2 = a_star.Node(pose=(1, 1))
        self.assertFalse(n2 in nodes)

    def test_less_than(self):
        n1 = a_star.Node()
        n1.cost = 1234.5678
        n2 = a_star.Node()
        n2.cost = 0.0

        self.assertTrue(n1 > n2)
        self.assertFalse(n1 < n2)


class TestAStar(unittest.TestCase):

    def test_get_neighbors8(self):

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
            neighbors = a_star.get_neighbors8(a_star.Node(pose=p), grid.shape)

            # check the correct number of poses was returned
            self.assertEqual(len(neighbors), len(poses[p]))

            # check the returned poses was as expected
            for n in neighbors:
                self.assertTrue(n.pose in poses[p])

    def test_get_neighbors4(self):

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
            neighbors = a_star.get_neighbors4(a_star.Node(pose=p), grid.shape)

            # check the correct number of poses was returned
            self.assertEqual(len(neighbors), len(poses[p]))

            # check the returned poses was as expected
            for n in neighbors:
                self.assertTrue(n.pose in poses[p])

    def test_plan(self):

        gridmap = np.zeros((5, 5))
        start = (0, 0)
        end = (4, 4)
        path = a_star.plan(gridmap, start, end)

        self.assertEquals(len(path), 5)


if __name__ == "__main__":
    unittest.main()
