#! /usr/bin/env python3
"""
Differential Drive Robot: Simulator
Iain Brookshaw
21 September 2019
"""
from odometry import DiffDriveOdometry as Odo

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import time


# SOME ROBOT CONSTANTS. TODO: Make args
_robot_wheelbase = 0.03       # meters
_robot_wheel_radius = 0.01    # meters
_robot_wheel_v_max = 0.2      # meters / second
_robot_max_motor_power = 1.0  # watts
_wheel_v_noise = 5.0          # +/- n% error in velocity calc
_robot_wheel_max_omega = _robot_wheel_v_max/_robot_wheel_radius  # rad/sec


class SimulationAnimation:
    """
    This is the 2d animated plot that simulated the movement and odometry of
    a differential drive robot. This class contains the odometry system, the
    the ground-truth calculation, noise generation, user interface callbacks
    and the plotting mechanics
    """

    def __init__(self, start_pose: tuple, wheelbase: float, delta_t: float) -> None:
        """
        :param start_pose: the (x,y,theta) original pose of the robot (m, m, rad)
        :param wheelbase:  the distance between the robot's two wheels (m)
        :param delta_t:    the simulation time-step (s)
        """
        self._odo = Odo(start_pose, wheelbase)  # the noisy computation
        self._gt = Odo(start_pose, wheelbase)   # the ground truth
        self._delta_t = delta_t

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
        self.ground_truth_path_x = [start_pose[0]]
        self.ground_truth_path_y = [start_pose[1]]
        self.ground_truth_path_theta = [start_pose[2]]
        #
        self.odo_path_x = [start_pose[0]]
        self.odo_path_y = [start_pose[1]]
        self.odo_path_theta = [start_pose[2]]

        # Plot data
        self.fig = plt.figure(figsize=(12, 12))
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

    def update_animation(self, dunno) -> list:
        """
        This method updates the simulation state (computing new odometry and gt)
        and updates the plot
        """

        # compute and update the ground truth
        l_v, r_v = self._get_wheel_velocities()
        true_pose = self._gt.update_pose(l_v, r_v, self._delta_t)
        self.ground_truth_path_x.append(true_pose[0])
        self.ground_truth_path_y.append(true_pose[1])
        self.ground_truth_path_theta.append(true_pose[2])

        # compute and update the noisy odometry pose
        l_nv, r_nv = self._add_noise_to_velocities(l_v, r_v)
        odom_pose = self._odo.update_pose(l_nv, r_nv, self._delta_t)
        self.odo_path_x.append(odom_pose[0])
        self.odo_path_y.append(odom_pose[1])
        self.odo_path_theta.append(odom_pose[2])

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

        return self._plot_lines

    def init_animation(self) -> list:
        self._ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10))
        #
        self._plot_lines = [
            self._ax.plot([], [], lw=2, ls='-', c='b',
                          label="Ground Truth")[0],
            self._ax.plot([], [], lw=2, ls=':', c='r',
                          label="Odometer Estimate")[0]
        ]

        self.connect_up_callbacks()

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

    def _get_wheel_velocities(self) -> tuple:
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

    def _add_noise_to_velocities(self, vr: float, vl: float) -> tuple:
        """
        generate a bit of noise between +/- noise percent
        """
        ln = 1 + np.random.uniform(low=-_wheel_v_noise, high=_wheel_v_noise)
        rn = 1 + np.random.uniform(low=-_wheel_v_noise, high=_wheel_v_noise)

        return (vl*ln, vr*rn)


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
