# Mobile Robot: Robot Architecture Dockerfile
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# to build: docker build -t myimagename .     # default 'Dockerfile'
#           docker build -f FirstDockerfile . # custom dockerfile
#
FROM osrf/ros:melodic-desktop-bionic

RUN apt-get update

# ROS/Gazebo dependencies for simulator communications and other ros-packages
RUN apt-get install -y \
    ros-melodic-gazebo-ros-pkgs \
    ros-melodic-gazebo-ros-control
#     ros-melodic-gazebo-ros-control \
#     ros-melodic-ros-control \
#     ros-melodic-ros-controllers

VOLUME [ "/mobile-robot-ros" ]

# Run the robot
CMD scripts/ros.bash

