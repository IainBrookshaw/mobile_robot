#! /usr/bin/env bash
#
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c) 2020, All Rights Reserved
# MIT License
# 
# Dockerized 'catkin_make'
#
pushd `pwd` > /dev/null
cd $( cd $(dirname $0); pwd)
source ../common.bash
ros_workspace="$(cd ../../../ning_ros_workspace; pwd)"
ros_log_path="/tmp/ning/ros"
chmod 777 $ros_log_path

ros_args=( "$@" )
# ros_args=("${args[@]:1}")  

ros_command=""
for arg in "${ros_args[@]}"; do
    ros_command="$ros_command $arg"
done
loginf "have command: $ros_command"

# docker run \
#     --rm \
#     -u $(id -u ${USER}):$(id -g ${USER}) \
#     --name="ning_ros_runner" \
#     \
#     -e ROS_COMMAND="${ros_command}" \
#     \
#     --env=ROSCONSOLE_STDOUT_LINE_BUFFERED="1" \
#     --volume $ros_workspace:"/ning_ros_workspace" \
#     --volume $ros_log_path:"/.ros" \
#     \
#     ningauble:ros_runner 
    
docker exec ning-gazebo "source /opt/ros/melodic/setup.bash && $ros_command"