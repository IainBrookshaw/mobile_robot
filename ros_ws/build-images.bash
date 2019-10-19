#! /usr/bin/env bash
#
# Mobile Robot: Make the Docker Containers
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
source scripts/mobile-robot.bash
_gazebo_out_file="/tmp/build-gazebo-image.txt"
_ros_out_file="/tmp/build-ros-image.txt"

function build_gazebo_container(){
    docker build -f gazebo.dockerfile -t $gazebo_docker_image_name . > $_gazebo_out_file
    if [ $? -ne 0 ]; then
        cat /tmp/build-gazebo-image.txt
        return 1
    else
        return 0
    fi
}

function build_ros_container(){
    docker build -f ros.dockerfile -t $ros_docker_image_name . > $_ros_out_file
    if [ $? -ne 0 ]; then
        cat /tmp/build-ros-image.txt
        return 1
    else
        return 0
    fi
}

echo "
 +--------------------------------------------------------------------------------+
 | Mobile Robot: Build Docker Images                                              |
 | Copyright (c) 2019                                                             |
 |                                                                                |
 | Build the Docker images for the Gazebo Simulations and ROS architecture.       |
 |                                                                                |
 |                    --- This may take some time ---                             |
 |                                                                                |
 +--------------------------------------------------------------------------------+
"


pushd `pwd` > /dev/null 2>&1

echo -ne "building Gazebo Container... "
build_gazebo_container
if [ $? -ne 0 ]; then
    echo "ERROR: could not build gazebo docker image"
    quit_with_popd 1
fi
echo
echo "done. Gazeo image is: \"$gazebo_docker_image_name\""

echo 
echo -ne "building ROS Container... "
build_ros_container
if [ $? -ne 0 ]; then
    echo "ERROR: could not build ros docker image"
    quit_with_popd 1
fi
echo
echo "done. ROS image is: \"$ros_docker_image_name\""

echo
echo "  ------------------------------------------------------------------------------"
quit_with_popd 0

