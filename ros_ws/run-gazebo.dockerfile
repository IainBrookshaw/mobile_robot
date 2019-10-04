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

# copy all the gazebo plugins into this container
RUN mkdir gazebo-plugin-libs
COPY ./gazebo-plugin-libs gazebo-plugin-libs
RUN export GAZEBO_PLUGIN_PATH=${GAZEBO_PLUGIN_PATH}:gazebo-plugin-libs

# copy all the gazebo worlds into this container
RUN mkdir worlds
COPY ./gazebo-worlds worlds

# todo: replace with master run script
CMD gzserver worlds/empty.world --verbose

