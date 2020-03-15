# 
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c), 2020, All Rights Reserved
# MIT License
#
# Dockerfile for the gazebo server side, including ROS melodic and all other
# components needed to stand up the robot simulation server
#
FROM osrf/ros:melodic-desktop-full-bionic

# system packages needed to build against Gazebo
RUN apt-get install -y \
    libgazebo9-dev

# install ROS packages necessary
RUN apt-get update && apt-get install -y \
    ros-melodic-octomap \
    ros-melodic-octomap-server

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

RUN mkdir /.gazebo
RUN mkdir /ning_ros_workspace
VOLUME "/.gazebo"
VOLUME "/ning_ros_workspace"

CMD [ "gzserver", "--verbose" ]
