#! /usr/bin/env bash
#
# Mobile Robot: Make the Docker Containers
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# This file contains some useful definitions, functions and names
# that make maintaining other build and run scripts easier. 
#
# Running this script on it's own will not do anything

# HOST file paths and URLs/URIs
root_file_path="$( cd "$(dirname "$0")" ; pwd -P )"
#
ros_network_static_ip="192.168.0"
ros_container_ip="$ros_network_static_ip.5"
gazebo_container_ip="$ros_network_static_ip.6"
ros_network="ros_net"

ros_master_uri="http://$gazebo_container_ip:12345" # todo: what are these magic numbers??


# ------------------------------------------------------------------------------
# Nice Colors :)

r="\e[31m"
g="\e[32m"
y="\e[33m"
b="\e[94m"
rs="\e[0m"

B="\e[1m"

echo_info="${B}[  ${b}INFO ${rs}${B}]:${rs}"
echo_ok="${B}[   ${g}OK  ${rs}${B}]:${rs}"
echo_warn="${B}[  ${y}WRN  ${rs}${B}]:${rs}"
echo_error="${B}[${r} ERROR ${rs}${B}]:${rs}"


# ------------------------------------------------------------------------------
# Images and Container Names

# Gazebo Container & Image
gazebo_docker_image_name="mobile-robot-gazebo"
gazebo_docker_run_container_name="mobile-robot-gazebo-run"
gazebo_docker_build_container_name="mobile-robot-gazebo-build"
#
gazebo_scripts_volume_host_path="$root_file_path/scripts"
gazebo_scripts_volume_name="/scripts"
#
gazebo_src_volume_host_path="$root_file_path"
gazebo_src_volume_name="/ros_ws"

# ROS Container & Image
ros_docker_image_name="mobile-robot-ros"
ros_docker_run_container_name="mobile-robot-ros-run"
ros_docker_build_container_name="mobile-robot-ros-build"
#
ros_scripts_volume_host_path="$root_file_path/scripts"
ros_scripts_volume_name="/scripts"
#
ros_src_volume_host_path="$root_file_path"
ros_src_volume_name="/ros_ws"


# ------------------------------------------------------------------------------
# Utility Functions

function quit_with_popd(){
    popd > /dev/null 2>&1
    exit $1
}

function cd_to_script_dir(){
    cd "$( cd "$(dirname "$0")" ; pwd -P )"
}

function set_ros_master_uri() {
    export ROS_MASTER_URI=$ros_master_uri
}

function create_ros_subnet() {
    docker network create --driver bridge --subnet=192.168.0.0/10 $ros_network
    return $?
}

function wait_for_roscore(){
    start=$(date +%s)
    until rostopic list; do 
        now=$(date +%s)
        if (( $now-$start > 5 )); then 
            echo "ERROR after 5 seconds, roscore did not come up!"
            return 1
        fi
        sleep 1
    done
    return 0
}