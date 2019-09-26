#! /usr/bin/env python3
"""
Differential Drive Robot: Odometry Testing
Iain Brookshaw
21 September 2019
"""
import unittest
from odometry import DiffDriveOdometry


class TestDiffDriveOdometry(unittest.TestCase):

    def test_compare_v(self):
        epsilon = 0.01
        self.assertTrue(DiffDriveOdometry._compare_v(0.01, 0.01, epsilon))
        self.assertTrue(DiffDriveOdometry._compare_v(0.01, 0.015, epsilon))

        self.assertFalse(DiffDriveOdometry._compare_v(0.01, 1, epsilon))
        self.assertFalse(DiffDriveOdometry._compare_v(0.01, 0.02, epsilon))

        self.assertFalse(DiffDriveOdometry._compare_v(-0.01, 0.01, epsilon))


        # ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()
