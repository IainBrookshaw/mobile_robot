#! /usr/bin/env python3
"""
Differential Drive Robot: Odometry
Iain Brookshaw
21 September 2019
"""
from typing import Tuple, Dict, List
import numpy as np


class DiffDriveOdometry:

    def __init__(self, start_pose: Tuple[float, float, float], wheelbase: float) -> None:
        self.wheelbase: float = wheelbase
        self._old_pose: Tuple[float, float, float] = start_pose

    def update_pose(self, v_l: float, v_r: float, delta_t: float, epsilon: float = 0.001) -> Tuple[float, float, float]:
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

        R = DiffDriveOdometry._compute_r(
            v_l,
            v_r
        )
        w = DiffDriveOdometry._compute_omega(
            v_l,
            v_r,
            self.wheelbase
        )
        icc = DiffDriveOdometry._compute_icc(
            R,
            self._old_pose[2],
            self._old_pose
        )
        new_theta = DiffDriveOdometry._compute_new_theta(
            self._old_pose[2],
            w,
            delta_t
        )
        new_x, new_y = DiffDriveOdometry._compute_new_corrdinate(
            self._old_pose,
            icc,
            w,
            delta_t
        )

        self._old_pose = (new_x, new_y, new_theta)
        return self._old_pose

    # ------------------------------------------------------------------------------------------------------------------
    # PRIVATE

    @staticmethod
    def _compare_v(v_l: float, v_r: float, epsilon: float) -> bool:
        """are the two velocities the same (diff < epsilon)?"""
        if np.sign(v_l) != np.sign(v_r):
            return False
        if abs(v_l - v_r) < epsilon:
            return True
        return False

    @staticmethod
    def _compute_r(v_l: float, v_r: float) -> float:
        """
        :param v_l: left wheel velocity (m/s)
        :param v_r: right wheel velocity (m/s)
        :returns the the radius of curvature
        """
        return (0.5 * (v_l + v_r)) / (v_r - v_l)

    @staticmethod
    def _compute_omega(v_l: float, v_r: float, wheelbase: float) -> float:
        """
        :param v_l: left wheel velocity (m/s)
        :param v_r: right wheel velocity (m/s)
        :param wheelbase: the rigid distance between the wheels (m)
        :returns: the rotational velocity around ICC
        """
        return (v_r-v_l)/wheelbase

    @staticmethod
    def _compute_icc(r: float, theta: float, old_pose: Tuple[float, float]) -> Tuple[float, float]:
        """
        :param r:        the radius of rotation around r (m)
        :param theta:    the old heading of the robot (rads)
        :param old_pose: the tuple that defines the old/current x,y pose of the robot (m)
        :returns: the global coordinates of the ICC (m)
        """
        return (
            old_pose[0] - r * np.sin(theta),
            old_pose[1] + r * np.cos(theta)
        )

    @staticmethod
    def _compute_new_theta(theta: float, omega: float, delta_t: float) -> float:
        """
        :param theta:   old/current heading of the robot (rad)
        :param omega:   rotational velocity around ICC (rad/sec)
        :param delta_t: time difference from old-new pose (sec) -- should be small
        """
        return theta + omega * delta_t

    @staticmethod
    def _compute_new_corrdinate(old_pose: tuple, icc: Tuple[float, float], omega: float, delta_t: float) -> Tuple[float, float]:
        """
        :param old_pose: the old/current pose of the robot (m,m,rad)
        :param icc:      the x,y global pose of the ICC (m,m)
        :param omega:    the rotational velocity of the robot around IC (rad)
        :param delta_t:  the time step from old/current to new (sec), should be small
        :returns: the new (x,y) global pose of the robot in meters
        """
        a = omega*delta_t

        R = np.matrix([
            [np.cos(a), -np.sin(a)],
            [np.sin(a),  np.cos(a)]
        ])
        X = np.matrix([
            old_pose[0] - icc[0],
            old_pose[1] - icc[1]
        ]).transpose()

        A = np.matrix([
            icc[0],
            icc[1]
        ]).transpose()

        new_pose_mat = R*X + A
        new_pose = (
            float(new_pose_mat[0]),
            float(new_pose_mat[1])
        )

        return new_pose
