#! /usr/bin/env python3
"""
Differential Drive Robot: Odometry
Iain Brookshaw
21 September 2019
"""

import numpy as np


class DiffDriveOdometry:

    def __init__(self, start_pose: tuple):
        self._old_pose = start_pose

    def update_pose(self, v_r: float, v_l: float, delta_t: float, epsilon=0.001: float):
        if DiffDriveOdometry._compare_v(v_r, v_l, epsilon):
            return (
                v_r*delta_t * np.cos(self._old_pose[2]),
                v_r*delta_t * np.sin(self._old_pose[2]),
                self._old_pose[2]
            )

        R = DiffDriveOdometry._compute_r(v_l, v_r)
        w = DiffDriveOdometry._compute_omega(v_l, v_r)
        icc = DiffDriveOdometry._compute_icc(R, self._old_pose)

        new_theta = DiffDriveOdometry._compute_new_theta(
            self._old_pose, w, delta_t)

        new_x, new_y = DiffDriveOdometry._compute_new_corrdinate(
            self._old_pose, icc, w, delta_t)

        self._old_pose = (new_x, new_y, new_theta)
        return self._old_pose

        # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _compare_v(v_l: float, v_r: float, epsilon: float):
        if np.sign(v_l) != np.sign(v_r):
            return False
        if abs(v_l - v_r) < epsilon:
            return True
        return False

    @staticmethod
    def _compute_r(v_l: float, v_r: float):
        pass

    @staticmethod
    def _compute_omega(v_l: float, v_r: float):
        pass

    @staticmethod
    def _compute_icc(r: float, old_pose: tuple):
        pass

    @staticmethod
    def _compute_new_theta(old_pose: tuple, omega: float, delta_t: float):
        pass

    @staticmethod
    def _compute_new_corrdinate(old_pose: tuple, icc: tuple, omega: float, delta_t: float):
        pass


if __name__ == "__main__":
    pass
