# Mobile Robot: Gazebo Build/Test Docker Image
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# Dockerfile for gazebo half of the project. This dockerfile defines the image 
# for _both_ building _and_ running the gazebo simulations, depending on the 
# arguments to the final script.
#
FROM osrf/ros:melodic-desktop-full-bionic

# system packages needed to build against Gazebo
RUN apt-get update && apt-get install -y \
    libgazebo9-dev \
    ros-melodic-gazebo-ros-control \
    ros-melodic-ros-controllers

# define the volumes we will mount from the host system
VOLUME ["/ros_ws", "/scripts"]

# run the build scripts
CMD /scripts/gazebo.bash

