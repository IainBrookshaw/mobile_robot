#! /usr/bin/env python3
"""
Differential Drive Robot: Simulator
Iain Brookshaw
21 September 2019
"""
from odometry import DiffDriveOdometry as Odo

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from typing import Tuple, Dict, List
import numpy as np
import time

# ----------------------------------------------------------------------------------------------------------------------
# Robot Chassis Constants
# TODO: Make args

_max_history: int = 1000
_robot_wheelbase: float = 0.03       # meters
_robot_wheel_radius: float = 0.01    # meters
_robot_wheel_v_max: float = 0.2      # meters / second
_robot_max_motor_power: float = 2.5  # watts
_wheel_v_noise: float = 0.05         # +/- n% error in velocity calc
_robot_wheel_max_omega: float = _robot_wheel_v_max/_robot_wheel_radius  # rad/sec

# ----------------------------------------------------------------------------------------------------------------------


class SimulationAnimation:
    """
    This is the 2d animated plot that simulated the movement and odometry of
    a differential drive robot. This class contains the odometry system, the
    the ground-truth calculation, noise generation, user interface callbacks
    and the plotting mechanics
    """

    def __init__(self, start_pose: Tuple[float, float, float], wheelbase: float, delta_t: float) -> None:
        """
        :param start_pose: the (x,y,theta) original pose of the robot (m, m, rad)
        :param wheelbase:  the distance between the robot's two wheels (m)
        :param delta_t:    the simulation time-step (s)
        """
        self._odo: Odo = Odo(start_pose, wheelbase)  # the noisy computation
        self._gt: Odo = Odo(start_pose, wheelbase)   # the ground truth
        self._delta_t: float = delta_t

        # robot speed from user (power to motors)
        self._total_motor_power = 0.0   # watts
        self._delta_motor_power = 0.01  # watts
        self._motor_prop = 0.0
        self._delta_prop = 0.01

        # motor encoder emulation
        self._left_encoder_true = 0
        self._right_encoder_true = 0
        self._left_encoder_noisy = 0
        self._right_encoder_noisy = 0

        # the plot-able paths for ground truth and estimated
        self.ground_truth_path_x: List = [start_pose[0]]
        self.ground_truth_path_y: List = [start_pose[1]]
        self.ground_truth_path_theta: List = [start_pose[2]]
        #
        self.odo_path_x: List = [start_pose[0]]
        self.odo_path_y: List = [start_pose[1]]
        self.odo_path_theta: List = [start_pose[2]]

        # Plot data
        self.fig: plt.Figure = plt.figure(figsize=(12, 12))
        self._display_text = None
        self._plot_lines = None
        self._ax = None

    # --------------------------------------------------------------------------
    # Animation Methods

    def connect_up_callbacks(self) -> None:
        """
        hooks up the keystroke callbacks to self.fig
        """
        self.fig.canvas.mpl_connect(
            'key_press_event',
            self._keystroke_handler_cb
        )

    def update_animation(self, dunno) -> List:  # TODO: WHAT IS THE dunno arg ??
        """
        This method updates the simulation state (computing new odometry and gt)
        and updates the plot
        """
        # compute and update the ground truth
        l_v, r_v = self._get_wheel_velocities()
        true_pose = self._gt.update_pose(l_v, r_v, self._delta_t)
        self._update_true_pose(true_pose)

        # compute and update the noisy odometry pose
        l_nv, r_nv = self._add_noise_to_velocities(l_v, r_v)
        odom_pose = self._odo.update_pose(l_nv, r_nv, self._delta_t)
        self._update_odom_pose(odom_pose)

        # update and return the plots
        if self._plot_lines:
            self._plot_lines[0].set_data(
                self.ground_truth_path_x,
                self.ground_truth_path_y
            )
            self._plot_lines[1].set_data(
                self.odo_path_x,
                self.odo_path_y
            )

        # print summary data:
        self._display_text.set_text(
            """
pose    = [{0:.2f}, {1:.2f}] m
heading = {2:.2f} degrees
wheel_v = [{3:.2f}, {4:.2f}] m/s
motor_p = {5:.2f} watts
""".format(
                true_pose[0], true_pose[1], np.degrees(true_pose[2]),
                l_v, r_v,
                self._total_motor_power
            ))

        return self._plot_lines

    def init_animation(self) -> List:
        self._ax = plt.axes(
            xlim=(-0.5, 0.5),  # todo: make args or global parameters
            ylim=(-0.5, 0.5))  # todo: make args or global parameters
        #
        self._plot_lines = [
            self._ax.plot([], [], lw=1, ls='-', c='b',
                          label="Ground Truth")[0],
            self._ax.plot([], [], lw=1, ls=':', c='r',
                          label="Odometer Estimate")[0]
        ]

        self.connect_up_callbacks()
        self._display_text = plt.text(-0.6, 0.5, "")

        plt.title("Differential Drive Robot: Odometry Simulation")
        plt.xlabel("Global X (meters)")
        plt.ylabel("Global Y (meters)")
        plt.legend()
        plt.grid()
        self._ax.set_aspect('equal', 'box')

        return self._plot_lines

    # --------------------------------------------------------------------------
    # User robot control keyboard callbacks

    def _keystroke_handler_cb(self, event) -> None:

        if event.key in ("up", "w"):
            self._total_motor_power += self._delta_motor_power
            if self._total_motor_power > _robot_max_motor_power:
                self._total_motor_power = _robot_max_motor_power

        elif event.key in ("left", "d"):
            self._motor_prop -= self._delta_prop
            if self._motor_prop < -1:
                self._motor_prop = -1.0

        elif event.key in ("right", "a"):
            self._motor_prop += self._delta_prop
            if self._motor_prop > 1:
                self._motor_prop = 1.0

        elif event.key in ("down", "s"):
            self._total_motor_power -= self._delta_motor_power
            if self._total_motor_power < -_robot_max_motor_power:
                self._total_motor_power = -_robot_max_motor_power

    # --------------------------------------------------------------------------
    # Private Methods

    def _get_wheel_velocities(self) -> Tuple[float, float]:
        """
        compute the current wheel velocities from the user settings of motor power
        """
        l_motor_power = self._total_motor_power * (self._motor_prop - 1)
        r_motor_power = self._total_motor_power * (self._motor_prop + 1)

        vl = (_robot_wheel_max_omega / _robot_max_motor_power) * \
            l_motor_power * _robot_wheel_radius
        vr = (_robot_wheel_max_omega / _robot_max_motor_power) * \
            r_motor_power * _robot_wheel_radius

        return (vl, vr)

    def _add_noise_to_velocities(self, vl: float, vr: float) -> Tuple[float, float]:
        """
        generate a bit of noise between +/- noise percent
        """
        ln = 1 + np.random.uniform(low=-_wheel_v_noise, high=_wheel_v_noise)
        rn = 1 + np.random.uniform(low=-_wheel_v_noise, high=_wheel_v_noise)

        return (vl*ln, vr*rn)

    def _update_true_pose(self, true_pose: Tuple[float, float, float]) -> None:
        if _max_history < len(self.ground_truth_path_x):
            self.ground_truth_path_x = self.ground_truth_path_x[:-2]
            self.ground_truth_path_y = self.ground_truth_path_y[:-2]
            self.ground_truth_path_theta = self.ground_truth_path_theta[:-2]

        self.ground_truth_path_x.append(true_pose[0])
        self.ground_truth_path_y.append(true_pose[1])
        self.ground_truth_path_theta.append(true_pose[2])

    def _update_odom_pose(self, odo_pose: Tuple[float, float, float]) -> None:
        if _max_history < len(self.odo_path_x):
            self.odo_path_x = self.odo_path_x[:-2]
            self.odo_path_y = self.odo_path_y[:-2]
            self.odo_path_theta = self.odo_path_theta[:-2]

        self.odo_path_x.append(odo_pose[0])
        self.odo_path_y.append(odo_pose[1])
        self.odo_path_theta.append(odo_pose[2])

    # ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # default values. TODO: make args
    start_pose = (0, 0, 0)
    wheelbase = 0.10
    delta_t = 0.01

    sim = SimulationAnimation(start_pose, wheelbase, delta_t)

    anim = animation.FuncAnimation(
        sim.fig,
        sim.update_animation,
        init_func=sim.init_animation
    )

    plt.show()
