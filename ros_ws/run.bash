#! /usr/bin/env bash
#
# Mobile Robot: Run ALL of the robot
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# Running this script will start up both the gazebo simulation and ROS architecture
# containers 
#
_this_dir="$( cd "$(dirname "$0")" ; pwd -P )"
pushd `pwd`
cd $_this_dir

# load all the constants
source scripts/mobile-robot.bash

# ----------------------------------------------------------------------------------------------------------------------
# FUNCTIONS

function close_containers() {

    echo -e "$echo_info\t stopping gazebo container"
    docker stop $gazebo_docker_run_container_name
    docker rm   $gazebo_docker_run_container_name

    echo -e "$echo_info\t stopping ros container"
    docker stop $ros_docker_run_container_name
    docker rm   $ros_docker_run_container_name

    echo -e "$echo_info\t terminating unused docker networks"
    yes | docker network prune
}

function run_gazebo() {

    echo

    docker run -d \
        --name $gazebo_docker_run_container_name \
        --volume $gazebo_src_volume_host_path:$gazebo_src_volume_name \
        --volume $gazebo_scripts_volume_host_path:$gazebo_scripts_volume_name \
        --env RUN_MODE="run" \
        --network=$ros_network \
        --ip $gazebo_container_ip \
        --env="DISPLAY" \
        --env="QT_X11_NO_MITSHM=1" \
        --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
        --runtime=nvidia \
        $gazebo_docker_image_name

    if [ $? -ne 0 ]; then 
        echo -e "$echo_error could not run the gazebo docker image"
        return 1
    fi

    echo -e "$echo_info\t Connecting the Gazebo container to the hosts X-Server"
    export containerId=$(docker ps -l -q)
    xhost +local:`docker inspect --format='{{ .Config.Hostname }}' $containerId`
    docker start $containerId

    return $?
}

function run_ros() {
    echo -e "$echo_info\t Running the ROS Architecture"
    docker run \
        --name $ros_docker_run_container_name \
        --volume $ros_scripts_volume_host_path:$ros_scripts_volume_name \
        --volume $ros_src_volume_host_path:$ros_src_volume_name \
        --env RUN_MODE="run" \
        --network $ros_network \
        --ip $ros_container_ip \
        $ros_docker_image_name
    
    return $?
}

# ----------------------------------------------------------------------------------------------------------------------
# MAIN


echo -e "$B
 +--------------------------------------------------------------------------------+
 | Mobile Robot: Run All                                                          |
 | Copyright (c) 2019                                                             |
 |                                                                                |
 | Running the mobile robot with Gazebo Simulation                                |
 +--------------------------------------------------------------------------------+ $rs
"

echo -e "$echo_info ${B}GERNERAL:$rs"
echo -e "$echo_info creating ros subnet for Docker containers... "
create_ros_subnet > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "$echo_error could not create ros subnet \"$ros_network\""
    close_containers 1
    quit_with_popd 1
fi
echo -e "$echo_ok ...done"

echo
echo -e "$echo_info ${B}GAZEBO:$rs"
echo -e "$echo_info starting gazebo container..."
run_gazebo > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo
    echo -e "$echo_error could not start gazebo docker container!"
    close_containers 1 > /dev/null 2>&1
    quit_with_popd 1
fi
echo -e "$echo_ok ...done"

echo
echo -e "$echo_info ${B}ROS:$rs"
echo -e "$echo_info starting ros container..."
run_ros > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo
    echo -e "$echo_error could not start ROS docker container!"
    close_containers 1 > /dev/null 2>&1
    quit_with_popd 1
fi
echo -e "$echo_ok ...done"
echo

echo -e "$echo_info Both ROS and Gazebo containers started and running."
echo -e "$echo_info Press ${g}${B}<enter>${rs} to stop both containers: "
read
echo -e "$echo_ok Run Finished"
echo -e "$echo_info Closing Gazebo and ROS Docker Containers..."
close_containers 0 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "$echo_error could not close containers cleanly!"
    quit_with_popd 1
fi
echo -e "$echo_ok ...done"
echo -e "${B}----------------------------------------------------------------------------------${rs}\n"
quit_with_popd $?