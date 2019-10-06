# Mobile Robot: Gazebo Build/Test Docker Image
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# Dockerfile for gazebo half of the project. This dockerfile defines the image 
# for _both_ building _and_ running the gazebo simulations, depending on the 
# arguments to the final script.
#
# To build by hand and debug run:
#   `docker run TODO
#
# To build all Gazebo plugins:
#   TODO
#
# To run the simulation:
#   TODO
#
# To build _and_ run the simulation:
#   TODO
#
FROM osrf/ros:melodic-desktop-full-bionic

# system packages needed to build against Gazebo
RUN apt-get install -y \
    libgazebo9-dev

# arg to pass to the gazebo.bash script; run as build or exe?
ARG mode

# run the build scripts
CMD gazebo/scripts/gazebo.bash $mode

