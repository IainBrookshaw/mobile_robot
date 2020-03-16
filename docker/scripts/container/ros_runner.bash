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

if [[ -z "${ROS_COMMAND}" ]]; then
    logerr "Please define the required ROS_COMMAND env var"
    exit 1
fi

${ROS_COMMAND}
if [ $? -ne 0 ]; then
    logerr "Command Failed"
    exit 1
fi
exit 0