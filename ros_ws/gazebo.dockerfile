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
RUN apt-get install -y \
    libgazebo9-dev

# define the volumes we will mount from the host system
VOLUME ["/ros_ws", "/scripts"]

# export the plugin libs path (necessary for running simulations, not build)
RUN export GAZEBO_PLUGIN_PATH=${GAZEBO_PLUGIN_PATH}:/gazebo/gazebo-plugin-libs

# run the build scripts
CMD /scripts/gazebo.bash

