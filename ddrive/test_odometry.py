#! /usr/bin/env python3
"""
Differential Drive Robot: Odometry Testing
Iain Brookshaw
21 September 2019
"""
import unittest
from ddrive.odometry import DDriveOdometry


class TestDiffDriveOdometry(unittest.TestCase):

    def test_compare_v(self):
        epsilon = 0.01
        self.assertTrue(DDriveOdometry._compare_v(0.01, 0.01, epsilon))
        self.assertTrue(DDriveOdometry._compare_v(0.01, 0.015, epsilon))

        self.assertFalse(DDriveOdometry._compare_v(0.01, 1, epsilon))
        self.assertFalse(DDriveOdometry._compare_v(0.01, 0.02, epsilon))

        self.assertFalse(DDriveOdometry._compare_v(-0.01, 0.01, epsilon))


        # ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()
