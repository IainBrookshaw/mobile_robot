# 
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c), 2020, All Rights Reserved
# MIT License
#
# General ROS Dockerfile for executing ros packages
FROM osrf/ros:melodic-desktop-full-bionic
ENV ROS_COMMAND="echo no ROS_COMMAND given"

COPY "scripts/common.bash" "/common.bash"
COPY "scripts/container/ros_runner.bash" "/ros_runner.bash"
RUN chmod 777 /ros_runner.bash

RUN apt-get update && apt-get install -y \
    liburdfdom-tools

RUN mkdir /.ros && \
    mkdir /ning_ros_workspace

RUN chmod 777 /.ros

VOLUME "/.ros"
VOLUME "/ning_ros_workspace"

WORKDIR "/ning_ros_workspace"
ENTRYPOINT ["bash", "-c", "/ros_runner.bash" ]