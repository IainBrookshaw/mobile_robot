#! /usr/bin/env python3
"""
Differential Drive Robot: Odometry
Iain Brookshaw
21 September 2019
"""

import numpy as np


class DiffDriveOdometry:

    def __init__(self, start_pose: tuple, wheelbase: float) -> None:
        self.wheelbase = wheelbase
        self._old_pose = start_pose

    def update_pose(self, v_l: float, v_r: float, delta_t: float, epsilon=0.001) -> tuple:
        """
        Compute the pose of the robot delta_t seconds after the last pose was computed.
        This is only going to be accurate for small steps of delta_t
        :param v_r:     float - the linear velocity of the right-hand wheel (m/s)
        :param v_l:     float - the linear velocity of the left-hand wheel  (m/s)
        :param delta_t: float - the time-step from the last pose measurement (sec)
        :param epsilon: float - the error allowable when computing v_r == v_l (m/s)
        :returns: the new pose (x',y',theta'), which is also set internally as the next _old_pose 
        """
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

    @staticmethod
    def encoder_to_velocity(delta_encoder_tick: int, max_encoder_tick: int, wheel_rad: float) -> float:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    # PRIVATE

    @staticmethod
    def _compare_v(v_l: float, v_r: float, epsilon: float) -> bool:
        if np.sign(v_l) != np.sign(v_r):
            return False
        if abs(v_l - v_r) < epsilon:
            return True
        return False

    @staticmethod
    def _compute_r(v_l: float, v_r: float) -> float:
        pass

    @staticmethod
    def _compute_omega(v_l: float, v_r: float) -> float:
        pass

    @staticmethod
    def _compute_icc(r: float, old_pose: tuple) -> tuple:
        pass

    @staticmethod
    def _compute_new_theta(old_pose: tuple, omega: float, delta_t: float) -> float:
        pass

    @staticmethod
    def _compute_new_corrdinate(old_pose: tuple, icc: tuple, omega: float, delta_t: float) -> tuple:
        pass
