#! /usr/bin/env bash
#
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c) 2020, All Rights Reserved
# MIT License
# 
# Dockerized 'rosrun'
# This should work exactly the same as regular rosrun, although it cannot start xserver apps
#
pushd `pwd` > /dev/null
cd $( cd $(dirname $0); pwd)
source ../common.bash
ros_workspace="$(cd ../../../ning_ros_workspace; pwd)"

args=( "$@" )
ros_package=$1
ros_executable=$2

ros_args=("${args[@]:2}")  

ros_args_str=""
for arg in "${ros_args[@]}"; do
    ros_args_str="$ros_args_str $arg"
done

docker run \
    --rm \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    --name="ning_ros_runner" \
    \
    --env=ROS_PACKAGE=$ros_package \
    --env=ROS_EXECUTABLE=$ros_executable \
    --env=ROS_RUN_ARGS="$ros_args_str" \
    \
    --env=ROSCONSOLE_STDOUT_LINE_BUFFERED="1" \
    --volume $ros_workspace:/ning_ros_workspace \
    \
    ningauble:ros_runner 
    