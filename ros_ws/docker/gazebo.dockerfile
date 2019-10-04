# Mobile Robot: Simulation Dockerfile
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# to build: docker build -t myimagename .     # default 'Dockerfile'
#           docker build -f FirstDockerfile . # custom dockerfile
#
# references:
#           https://hub.docker.com/_/gazebo
#           http://gazebosim.org/tutorials?tut=plugins_hello_world&cat=write_plugin
#           http://gazebosim.org/tutorials?tut=guided_i6
#
FROM osrf/ros:melodic-desktop-full-bionic

RUN apt-get install -y \
    libgazebo9-dev

# Build all the Gazebo plugins used by this mobile robot
RUN scripts/build-gazebo-plugins.bash

# Export the path to the plugins



CMD gazebo

