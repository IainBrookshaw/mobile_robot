# Mobile Robot: Gazebo Build/Test Docker Image
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# This can be run 'headless', we will not actuall call the gazebo simulator in this
# dockerfile. Here we do the build and testing harness
#
# TODO: make part of the runtime docker image
#
FROM osrf/ros:melodic-desktop-full-bionic

# system packages needed to build against Gazebo
RUN apt-get install -y \
    libgazebo9-dev

# run the build scripts
CMD scripts/build-gazebo-plugins.bash
