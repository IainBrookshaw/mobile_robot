# 
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c), 2020, All Rights Reserved
# MIT License
#
# General ROS Dockerfile for executing ros packages
FROM osrf/ros:melodic-desktop-full-bionic

COPY "scripts/common.bash" "/common.bash"
COPY "scripts/container/ros_runner.bash" "/common.bash"


RUN mkdir /.ros && \
    mkdir /ning_ros_workspace

VOLUME "/.ros"
VOLUME "/ning_ros_workspace"

ENTRYPOINT ["bash", "-c", "/ros_runner.bash" ]