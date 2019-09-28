#! /usr/bin/env python3
"""
Differential Drive Robot: Simulator
Iain Brookshaw
21 September 2019

MIT License, Copyright (c) 2019, All Rights Reserved
"""
from odometry import DDriveOdometry as Odo

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from typing import Tuple, Dict, List
import numpy as np
import time


class SimulationConfig:
    """
    There are a lot of simulation configuration variables. For simplicity, we 
    are bundling them up in this class
    """

    def __init(self):
        self.start_pose: Tuple(float, float) = (0.0, 0.0)
        # the simulation time-step (sec)
        self.delta_t: float = 0.1

        # max wheel rotational speed (rad/sec)
        self.robot_wheel_max_omega: float = 0.0
        self.robot_max_motor_power: float = 0.0  # maximum motor poser (watts)
        self.robot_wheelbase: float = 0.0       # wheel separation (meters)

        self.wheel_noise = 0.05  # how much wheel velocity noise to +/-
        self.delta_wheel_motor: float = 0.1  # change in motor power for each keystroke

        self.colors: Dict = {}  # display colors
        self.minimum_min_x = -1.0
        self.minimum_max_x = 1.0
        self.minimum_min_y = -1.0
        self.minimum_max_y = 1.0

# ----------------------------------------------------------------------------------------------------------------------


class SimulationAnimation:
    """
    This is the 2d animated plot that simulated the movement and odometry of
    a differential drive robot. This class contains the odometry system, the
    the ground-truth calculation, noise generation, user interface callbacks
    and the plotting mechanics
    """

    def __init__(self, config: SimulationConfig) -> None:
        """
        :param config: the SimulatioNConfig object that defines all the constants 
        for this simulation
        """
        self._config = config

        # the noisy computation and the ground truth
        self._odo: Odo = Odo(config.start_pose, config.robot_wheelbase)
        self._gt: Odo = Odo(config.start_pose, config.robot_wheelbase)

        # robot speed from user (power to motors)
        self._motor_prop = 0.5

        # the plot-able paths for ground truth and estimated
        self.ground_truth_path_x: List = [config.start_pose[0]]
        self.ground_truth_path_y: List = [config.start_pose[1]]
        self.ground_truth_path_theta: List = [config.start_pose[2]]
        #
        self.odo_path_x: List = [config.start_pose[0]]
        self.odo_path_y: List = [config.start_pose[1]]
        self.odo_path_theta: List = [config.start_pose[2]]

        # Plot data and turn off ALL keybindings. the init will re-establish this
        self.fig: plt.Figure = plt.figure(
            figsize=(12, 12),
            facecolor=config.colors["background"]
        )
        self._display_text = None
        self._plot_lines = None
        self._ax = None

    # --------------------------------------------------------------------------
    # Animation Methods

    def connect_up_callbacks(self) -> None:
        """
        turns off existing key-callbacks and 
        hooks up the custom keystroke callbacks to self.fig
        """
        self.fig.canvas.mpl_disconnect(
            self.fig.canvas.manager.key_press_handler_id)

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
        true_pose = self._gt.update_pose(l_v, r_v, self._config.delta_t)
        self._update_true_pose(true_pose)

        # compute and update the noisy odometry pose
        l_nv, r_nv = self._add_noise_to_velocities(
            self._config.wheel_noise, l_v, r_v)

        odom_pose = self._odo.update_pose(l_nv, r_nv, self._config.delta_t)

        self._update_odom_pose(odom_pose)

        # compute axes limits
        self._re_scale_axes()

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

        # update the wheel and robot patches
        self._update_patches()

        # print summary data:
        self._display_text.set_text(
            """
pose       = [{0:.2f}, {1:.2f}] mm, {2:.2f} degrees
wheel_v    = [{3:.2f}, {4:.2f}] m/s, 
motor_p    = {5:.2f} watts
pose error = {6:.2f} mm by, Heading Error = {7:.2f} degrees
""".format(
                true_pose[0]*1000, true_pose[1]*1000, np.degrees(true_pose[2]),
                l_v, r_v,
                self._total_motor_power,
                1000.0*self._compute_pose_error_abs(odom_pose, true_pose),
                np.degrees(true_pose[2] - odom_pose[2])
            ))
        self._display_text.set_color(self._config.colors["text_color"])
        self._display_text.set_backgroundcolor(self._config.colors["bg_color"])

        return self._plot_lines

    def init_animation(self) -> List:

        self._ax = plt.axes(
            xlim=(-0.5, 0.5),  # todo: make args or global parameters
            ylim=(-0.5, 0.5))  # todo: make args or global parameters
        #
        self._ax.set_facecolor(self._config.colors["text_color"])
        self._ax.xaxis.label.set_color(self._config.colors["text_color"])
        self._ax.yaxis.label.set_color(self._config.colors["text_color"])
        #
        self._ax.spines['bottom'].set_color(self._config.colors["text_color"])
        self._ax.spines['left'].set_color(self._config.colors["ext_color"])
        self._ax.spines['right'].set_color(self._config.colors["text_color"])
        self._ax.spines['top'].set_color(self._config.colors["text_color"])
        #
        self._ax.tick_params(
            axis='x', colors=self._config.colors["text_color"])
        self._ax.tick_params(
            axis='y', colors=self._config.colors["text_color"])

        self._plot_lines = [
            self._ax.plot([], [], lw=1, ls='-',
                          color=self._config.colors["ground_truth"],
                          label="Ground Truth Pose")[0],
            #
            self._ax.plot([], [], lw=2, ls=':',
                          color=self._config.colors["odometry"],
                          markersize=5,
                          label="Odometer Estimate Pose")[0]
        ]

        self.connect_up_callbacks()
        self._display_text = self._ax.text(0, 0, "",
                                           horizontalalignment='left',
                                           backgroundcolor=self._config.colors["background"],
                                           color=self._config.colors["text_color"],
                                           linespacing=1.2,
                                           fontfamily='monospace',
                                           fontsize=12)

        plt.title("Differential Drive Robot: Odometry Simulation",
                  fontsize=20, color=self._config.colors["text_color"])

        plt.xlabel("Global X (meters)", fontsize=15)
        plt.ylabel("Global Y (meters)", fontsize=15)
        leg = self._ax.legend(loc='upper right',
                              fontsize=15,
                              fancybox=False,
                              numpoints=1)
        leg.get_frame().set_facecolor(self._config.colors["background"])

        for text in leg.get_texts():
            text.set_color(self._config.colors["text_color"])

        plt.grid()
        self._ax.set_aspect('equal', 'box')

        return self._plot_lines

    # --------------------------------------------------------------------------
    # User robot control keyboard callbacks

    def _keystroke_handler_cb(self, event) -> None:

        if event.key in ("up", "w"):
            self._config.total_motor_power += self._config.delta_motor_power
            if self._config.total_motor_power > self._config.robot_max_motor_power:
                self._config.total_motor_power = self._config.robot_max_motor_power

        elif event.key in ("left", "d"):
            self._motor_prop -= self._delta_prop
            if self._motor_prop < -1:
                self._motor_prop = -1.0

        elif event.key in ("right", "a"):
            self._motor_prop += self._delta_prop
            if self._motor_prop > 1:
                self._motor_prop = 1.0

        elif event.key in ("down", "s"):
            self._total_motor_power -= self._config.delta_motor_power
            if self._total_motor_power < -self._config.robot_max_motor_power:
                self._total_motor_power = -self._config.robot_max_motor_power

    # --------------------------------------------------------------------------
    # Private Methods

    def _update_patches(self):
        """
        update the robot wheel image patches
        TODO: Implement
        """
        pass

        # TODO: show direction arrow
        # self._true_dir_arrow = plt.Arrow(
        #     0, 0, 0, 0, label="Ground Truth Heading")
        # self._odo_dir_arrow = plt.Arrow(
        #     0, 0, 0, 0, label="Odometer Estimate Heading")

        # self._plot_lines.append(self._true_dir_arrow)
        # self._plot_lines.append(self._odo_dir_arrow)

        # update heading arrows
        # gt_heading_vector = self._compute_heading_vector(
        #     true_pose, true_pose[2])
        # odo_heading_vector = self._compute_heading_vector(
        #     odom_pose, odom_pose[2])
        #
        # self._plot_lines[2].set_data(
        #     true_pose[0], true_pose[1], gt_heading_vector[0], gt_heading_vector[1])
        # self._plot_lines[3].set_data(
        #     odom_pose[0], odom_pose[1], odo_heading_vector[0], odo_heading_vector[1])

    def _get_wheel_velocities(self) -> Tuple[float, float]:
        """
        compute the current wheel velocities from the user settings of motor power
        """
        l_motor_power = self._total_motor_power * (self._motor_prop - 1)
        r_motor_power = self._total_motor_power * (self._motor_prop + 1)

        vl = (self._config.robot_wheel_max_omega / self._config.robot_max_motor_power) * \
            l_motor_power * self._config.robot_wheel_radius
        vr = (self._config.robot_wheel_max_omega / self._config.robot_max_motor_power) * \
            r_motor_power * self._config.robot_wheel_radius

        return (vl, vr)

    def _add_noise_to_velocities(self, wheel_noise: float, vl: float, vr: float) -> Tuple[float, float]:
        """
        generate a bit of noise between +/- noise percent
        """
        ln = 1 + np.random.uniform(low=-wheel_noise, high=wheel_noise)
        rn = 1 + np.random.uniform(low=-wheel_noise, high=wheel_noise)
        return (vl*ln, vr*rn)

    def _update_true_pose(self, true_pose: Tuple[float, float, float]) -> None:
        if self._config.max_history < len(self.ground_truth_path_x):
            self.ground_truth_path_x = self.ground_truth_path_x[: -2]
            self.ground_truth_path_y = self.ground_truth_path_y[: -2]
            self.ground_truth_path_theta = self.ground_truth_path_theta[: -2]

        self.ground_truth_path_x.append(true_pose[0])
        self.ground_truth_path_y.append(true_pose[1])
        self.ground_truth_path_theta.append(true_pose[2])

    def _update_odom_pose(self, odo_pose: Tuple[float, float, float]) -> None:
        if self._config.max_history < len(self.odo_path_x):
            self.odo_path_x = self.odo_path_x[: -2]
            self.odo_path_y = self.odo_path_y[: -2]
            self.odo_path_theta = self.odo_path_theta[: -2]

        self.odo_path_x.append(odo_pose[0])
        self.odo_path_y.append(odo_pose[1])
        self.odo_path_theta.append(odo_pose[2])

    def _compute_pose_error_abs(self, odo_pose, true_pose) -> float:
        dx = odo_pose[0] - true_pose[0]
        dy = odo_pose[1] - true_pose[1]
        return float(np.sqrt(dx**2 + dy**2))

    def _compute_heading_vector(self, pose, theta):
        return (
            pose[0] + 0.25 * np.cos(theta),
            pose[1] + 0.25 * np.sin(theta)
        )

    def _get_axes_limits(self, arr):
        arr_min = 1e6
        arr_max = -1e6
        for entry in arr:
            if arr_min > entry:
                arr_min = entry
            if arr_max < entry:
                arr_max = entry

        return (1.1*arr_min, 1.1*arr_max)

    def _re_scale_axes(self):
        gt_min_x, gt_max_x = self._get_axes_limits(self.ground_truth_path_x)
        gt_min_y, gt_max_y = self._get_axes_limits(self.ground_truth_path_y)
        #
        od_min_x, od_max_x = self._get_axes_limits(self.odo_path_x)
        od_min_y, od_max_y = self._get_axes_limits(self.odo_path_y)

        min_x = gt_min_x if gt_min_x < od_min_x else od_min_x
        min_y = gt_min_y if gt_min_y < od_min_y else od_min_y
        max_x = gt_max_x if gt_max_x < od_max_x else od_max_x
        max_y = gt_max_y if gt_max_y < od_max_y else od_max_y

        if max_x < self._config.minimum_max_x:
            max_x = self._config.minimum_max_x

        if min_x > self._config.minimum_min_x:
            min_x = self._config.minimum_min_x

        if max_y < self._config.minimum_max_y:
            max_y = self._config.minimum_max_y

        if min_y > self._config.minimum_min_y:
            min_y = self._config.minimum_min_y

        self._ax.set_xlim(min_x, max_x)
        self._ax.set_ylim(min_y, max_y)
        self._display_text.set_position((.95*min_x, 0.95*min_y))
