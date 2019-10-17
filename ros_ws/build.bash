#! /usr/bin/env bash
#
# Mobile Robot: Run All the Build Docker Containers
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# Running this script will build both the gazebo and ros components of this 
# project. We mount the source code and build dirs as volumes to the mobile
# robot docker image
#
# You must run the `build-docker-images.bash` script first for this to work

source scripts/mobile-robot.bash

_this_dir="$( cd "$(dirname "$0")" ; pwd -P )"
pushd `pwd` > /dev/null 2>&1
cd $_this_dir


# ----------------------------------------------------------------------------------------------------------------------
# FUNCTIONS

function quit(){
    docker rm $gazebo_docker_build_container_name > /dev/null 2>&1
    docker rm $ros_docker_build_container_name > /dev/null 2>&1
    quit_with_popd
}

function build_gazebo(){

    docker run \
        --name   $gazebo_docker_build_container_name \
        --volume $gazebo_scripts_volume_host_path:$gazebo_scripts_volume_name \
        --volume $gazebo_src_volume_host_path:$gazebo_src_volume_name \
        --env RUN_MODE=$1 \
        $gazebo_docker_image_name

    return $?
}

function build_ros(){
    docker run \
        --name $ros_docker_build_container_name \
        --volume $ros_scripts_volume_host_path:$ros_scripts_volume_name \
        --volume $ros_src_volume_host_path:$ros_src_volume_name \
        --env  RUN_MODE=$1 \
        $ros_docker_image_name

    return $?
}

# ----------------------------------------------------------------------------------------------------------------------
# MAIN

echo "---------------------------------------------------------------------------------"
echo "Mobile Robot: Build All"
echo "Copyright (c) 2019"
echo 
echo "Building All Gazebo Plugins and ROS Packages"
echo "using a Docker build environment"
echo "---------------------------------------------------------------------------------"
echo 

build_flag="build"
if [ "$1" == "clean" ]; then
    echo "Building ROS and Gazebo with \"clean\" flag. This will take a while"
    build_flag="build-clean"
fi

echo "GAZEBO:"
echo "Building all Gazebo plugins"
build_gazebo $build_flag
if [ $? -ne 0 ]; then
    echo "ERROR: gazebo build failed!"
    quit 1
fi
echo "Gazebo Build Done"

echo -e "\nROS:"
echo "Building ROS Architecture"
build_ros $build_flag
if [ $? -ne 0 ]; then
    echo "ERROR: ros build failed"
    quit 1
fi

echo "ROS Build Done"
echo "---------------------------------------------------------------------------------" 
quit 0