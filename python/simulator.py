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

        self._odo = Odo(start_pose, wheelbase)
        self._delta_t = delta_t

        # robot speed from user
        self._velocity_mag = 0.1  # meters/sec
        self._delta_velocity_mag = 0.01  # meters/sec
        self._velocity_theta = 0.0  # radians
        self._delta_velocity_theta = np.radians(0.1)  # radians

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

        # compute the true and noisy encoders and convert the noisy values to velocities
        l_encoder = self._emulate_left_wheel_encoder()
        l_enc_noisy = l_encoder + \
            self._generate_encoder_noise(
                0.1)  # Todo: hardcoded noise magnitude
        #
        r_encoder = self._emulate_right_wheel_encoder()
        r_enc_noisy = r_encoder + \
            self._generate_encoder_noise(
                0.1)  # Todo: hardcoded noise magnitude
        #
        v_l = self._encoder_to_velocity(self._left_encoder_noisy, l_enc_noisy)
        v_r = self._encoder_to_velocity(self._right_encoder_noisy, r_enc_noisy)

        # compute and update the odometry estimate
        odo_pose = self._odo.update_pose(v_l, v_r, self._delta_t)
        self.odo_path_x.append(odo_pose[0])
        self.odo_path_y.append(odo_pose[1])
        self.odo_path_theta.append(odo_pose[2])
        #
        if self._plot_lines:
            self._plot_lines[1].set_data(
                self.odo_path_x,
                self.odo_path_y
            )

        # compute and update the ground truth calculation
        true_pose = self._update_true_pose(l_encoder, r_encoder)
        self.ground_truth_path_x.append(true_pose[0])
        self.ground_truth_path_y.append(true_pose[1])
        self.ground_truth_path_theta.append(true_pose[2])
        #
        if self._plot_lines:
            self._plot_lines[0].set_data(
                self.ground_truth_path_x,
                self.ground_truth_path_y
            )

        return self._plot_lines

    def init_animation(self) -> list:
        print("DBG *** creating axes")
        self._ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10))
        #
        self._plot_lines = [
            self._ax.plot([], [], lw=2, ls='-', c='b')[0],  # Ground truth
            self._ax.plot([], [], lw=2, ls=':', c='r')[0]   # Estimate
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

    def _keystroke_handler_cb(self, event):  # -> None:

        if event.key in ("up", "w"):
            self._velocity_mag += self._delta_velocity_mag
            print("DBG *** Up Key! velocity = {} m/s at {} deg".format(
                self._velocity_mag, np.degrees(self._velocity_theta)))

        elif event.key in ("left", "d"):
            self._velocity_theta += self._delta_velocity_theta
            print("DBG *** Left Key! velocity = {} m/s at {} deg".format(
                self._velocity_mag, np.degrees(self._velocity_theta)))

        elif event.key in ("right", "a"):
            self._velocity_theta -= self._delta_velocity_theta
            print("DBG *** Right Key! velocity = {} m/s at {} deg".format(
                self._velocity_mag, np.degrees(self._velocity_theta)))

        elif event.key in ("down", "s"):
            self._velocity_mag -= self._delta_velocity_mag
            print("DBG *** Down Key! velocity = {} m/s at {} deg".format(
                self._velocity_mag, np.degrees(self._velocity_theta)))

    # --------------------------------------------------------------------------
    # Private Methods

    def _emulate_left_wheel_encoder(self) -> float:
        return 1.0  # TODO: implement

    def _emulate_right_wheel_encoder(self) -> float:
        return 1.0  # TODO: implement

    def _encoder_to_velocity(self, old_encoder, new_encoder) -> float:
        return 0.0  # TODO: implement

    def _generate_encoder_noise(self, magnitude: float) -> float:
        return 0.0  # TODO: implement

    def _update_true_pose(self, l_enc, r_enc) -> tuple:
        return (0, 0, 0)  # TODO: implement


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
