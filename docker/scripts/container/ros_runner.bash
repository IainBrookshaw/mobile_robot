#! /usr/bin/env bash
#
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c) 2020, All Rights Reserved
# MIT License
#
source /common.bash
source /opt/ros/melodic/setup.bash
if [ -f /ning_ros_workspace/devel/setup.bash ]; then
    source /ning_ros_workspace/devel/setup.bash
else
    logwrn "unable to find ning_ros_workspace/devel/setup.bash!"
fi

if [[ -z "${ROS_PACKAGE}" ]]; then
    logerr "Please define the required ROS package"
    exit 1
fi
if [[ -z "${ROS_EXECUTABLE}" ]]; then
    logerr "Please define the required ROS executable"
    exit 1
fi
rospack find $ROS_PACKAGE 
if [ $? -ne 0 ]; then
    logerr "the package \"$ROS_PACKAGE\" is not a valid ROS package"
    exit 1
fi
if ! rosrun $ROS_PACKAGE $ROS_EXECUTABLE $ROS_RUN_ARGS; then
    logerr "unable to 'rosrun $ROS_PACKAGE $ROS_EXECUTABLE"
    exit 1
fi
exit 0