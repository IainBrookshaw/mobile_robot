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
ENV ROSPACKAGE "not-a-package"
ENV LAUNCHFILE "not/a/launchfile"
ENV LIBGL_ALWAYS_INDIRECT "1"

# system packages needed to build against Gazebo
RUN apt-get install -y \
    libgazebo9-dev

# install ROS packages necessary
RUN apt-get update && apt-get install -y \
    liburdfdom-tools \
    ros-melodic-octomap \
    ros-melodic-octomap-server

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

# Gazebo logging
RUN mkdir /.gazebo && chmod -R 777 /.gazebo
RUN mkdir /.ros    && chmod -R 777 /.ros
VOLUME "/.gazebo"
VOLUME "/.ros"

# Source Code and end-user
RUN mkdir /ros_workspace && chmod 777 /ros_workspace
VOLUME "/ros_workspace"
VOLUME "/ning-tools"

WORKDIR "/ros_workspace"
CMD [ "/bin/bash", "-c", "source /ros_workspace/devel/setup.bash && roslaunch $ROSPACKAGE $LAUNCHFILE" ]
# CMD [ "sh", "-c", "echo", "package = $ROSPACKAGE launchfile = $LAUNCHFILE" ]
