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

source scripts/mobile-robot.bash

# ----------------------------------------------------------------------------------------------------------------------
# FUNCTIONS

function close_containers() {

    echo -e "\trun.bash: stopping gazebo container"
    docker stop $gazebo_docker_run_container_name
    docker rm   $gazebo_docker_run_container_name

    echo -e "\trun.bash: stopping ros container"
    docker stop $ros_docker_run_container_name
    docker rm   $ros_docker_run_container_name

    echo -e"\tterminating unused docker networks"
    yes | docker network prune
}

function run_gazebo() {

    echo

    docker run \
        --name $gazebo_docker_run_container_name \
        --volume $gazebo_src_volume_host_path:$gazebo_src_volume_name \
        --volume $gazebo_scripts_volume_host_path:$gazebo_scripts_volume_name \
        --env RUN_MODE="run" \
        --env="DISPLAY" \
        --env="QT_X11_NO_MITSHM=1" \
        --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
        $gazebo_docker_image_name > /dev/null 2>&1

        # --net $ros_net \
        # --ip "$ros_network_static_ip".10 \
        #

    if [ $? -ne 0 ]; then 
        echo "ERROR: could not run the gazebo docker image"
        return 1
    fi

    echo -e "\trun_gazebo: Connecting the Gazebo container to the hosts X-Server"
    export containerId=$(docker ps -l -q)
    xhost +local:`docker inspect --format='{{ .Config.Hostname }}' $containerId`
    docker start $containerId

    return $?
}

function run_ros() {
    echo -e "\trun_ros: Running the ROS Architecture"
    docker run \
        --name $ros_run_container_name \ 
        --volume ../ros_ws \
        --net $ros_network \
        --ip "$ros_network_static_ip".11 \
        $ros_img_name
    return 0
}

# ----------------------------------------------------------------------------------------------------------------------
# MAIN


echo "
 +--------------------------------------------------------------------------------+
 | Mobile Robot: Run All                                                          |
 | Copyright (c) 2019                                                             |
 |                                                                                |
 | Running the mobile robot with Gazebo Simulation                                |
 +--------------------------------------------------------------------------------+
"
echo
echo "GERNERAL:"
echo -en "creating ros subnet for Docker containers... "
create_ros_subnet
if [ $? -ne 0 ]; then
    echo "could not create ros subnet \"$ros_network\""
    close_containers 1
    quit_with_popd 1
fi
echo "done"

echo
echo "GAZEBO:"
echo -en "starting gazebo container..."
run_gazebo > /dev/null 2>&1 &
if [ $? -ne 0 ]; then
    echo
    echo "ERROR: could not start gazebo docker container!"
    close_containers 1 > /dev/null 2>&1
    quit_with_popd 1
fi
echo " done"

echo
echo "ROS:"
echo -en "starting ros container..."
run_ros > /dev/null 2>&1 &
if [ $? -ne 0 ]; then
    echo
    echo "ERROR: could not start ROS docker container!"
    close_containers 1 > /dev/null 2>&1
    quit_with_popd 1
fi
echo " done"
echo

echo "Both ROS and Gazebo containers started and running."
read -ep "**** Press <enter> to stop both containers: "
echo "Run Finished, closing both ROS and Gazebo containers..."
echo

echo
echo "Closing Gazebo and ROS Docker Containers"
echo "----------------------------------------------------------------------------------"
close_containers 0 > /dev/null 2>&1
quit_with_popd $?
