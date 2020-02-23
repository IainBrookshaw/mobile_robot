#! /usr/bin/env python3
"""
Mobile Robot Path Planning: A* Testing
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""

import unittest
import numpy as np
import matplotlib.pyplot as plt

from path_planning.planner import GridMapPlanner, Node
from path_planning.a_star import AStar


class TestAStar(unittest.TestCase):

    def setUp(self):
        self.planner = AStar()

    def test_g(self):
        node1 = Node(pose=(0, 0))
        node2 = Node(pose=(1, 1))
        node3 = Node(pose=(2, 2))
        #
        node1.parent = None
        node2.parent = node1
        node3.parent = node2
        #
        node1.g = 0
        node2.g = np.sqrt(2)
        node3.g = 2*np.sqrt(2)

        start = node1

        g_costs = [
            (self.planner._g(node1, start), 0),
            (self.planner._g(node2, start), np.sqrt(2)),
            (self.planner._g(node3, start), 2*np.sqrt(2))
        ]
        for g in g_costs:
            self.assertAlmostEqual(g[0], g[1])

    def test_h(self):

        node = Node(pose=(0, 0))
        goal = Node(pose=(10, 10))

        actual = self.planner._h(node, goal)
        expected = np.sqrt(10*10 + 10*10)

        self.assertAlmostEqual(expected, actual)

    def test_plan(self):

        gridmap = np.zeros((5, 5))
        start = (0, 0)
        end = (4, 4)
        try:
            path = self.planner.plan(gridmap, start, end)
        except Exception as e:
            self.fail(e)

        self.assertEqual(len(path), 5)

        self.planner.plot_path(
            gridmap,
            GridMapPlanner.marshal_pose_list_for_plot(path),
            GridMapPlanner.marshal_pose_list_for_plot(self.planner.visited)
        )
        plt.show()


if __name__ == "__main__":
    unittest.main()
