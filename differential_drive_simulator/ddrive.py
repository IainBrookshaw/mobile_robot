#! /usr/bin/env python3
"""
Differential Drive Robot: Main Program
Iain Brookshaw
21 September 2019
"""
from odometry import DiffDriveOdometry as Odo

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from typing import Tuple, Dict, List
import numpy as np
import argparse
import time

# ----------------------------------------------------------------------------------------------------------------------
# Robot Chassis Constants
# When run as an executable, these may be set by the args

_max_history: int = 1000
_robot_wheelbase: float = 0.03       # meters
_robot_wheel_radius: float = 0.01    # meters
_robot_wheel_v_max: float = 0.2      # meters / second
_robot_max_motor_power: float = 2.5  # watts
_wheel_v_noise: float = 0.5          # +/- n% error in velocity calc
_robot_wheel_max_omega: float = _robot_wheel_v_max/_robot_wheel_radius  # rad/sec

#
_minimum_max_x = 0.1
_minimum_min_x = -0.1
_minimum_max_y = 0.1
_minimum_min_y = -0.1

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-dt", "--delta_t", type=float,
                        help="simulation delta-t")
    parser.add_argument("--history", type=float,
                        help="the robot plotting history in seconds")
    parser.add_argument("--wheelbase", type=float,
                        help="the robot's wheelbase in meters")
    parser.add_argument("--radius", type=float,
                        help="the robot's wheel radius in meters")
    parser.add_argument("--noise", type=float,
                        help="wheel odometer velocity noise per step (+/- %)")

    parser.add_argument("--dark", action='store_true', help="use dark theme")

    args = parser.parse_args()
    if args.delta_t:
        _delta_t = args.delta_t
    if args.wheelbase:
        _robot_wheelbase = args.wheelbase
    if args.radius:
        _robot_wheel_radius = args.radius
    if args.noise:
        _wheel_v_noise = args.noise

    if args.history:
        _max_history = int(round(args.history * _delta_t))

    # Aesthetics
    _bg_color = "#0d0d0f" if args.dark else "White"
    _text_color = "#fce5c7" if args.dark else _bg_color
    _robot_color = "DodgerBlue" if args.dark else "Blue"
    _ground_truth_color = "DodgerBlue" if args.dark else "Blue"
    _odo_path_color = "Coral" if args.dark else "Red"

    # The Simulation
    # TODO: make the input args non-global
    sim = SimulationAnimation(start_pose, _robot_wheelbase, _delta_t)

    anim = animation.FuncAnimation(
        sim.fig,
        sim.update_animation,
        init_func=sim.init_animation
    )

    plt.show()
