# Mobile Robot: Make the Docker Containers
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
source scripts/mobile-robot.bash

function build_gazebo_container(){
    docker build -f gazebo.dockerfile -t $gazebo_docker_image_name .
}

function build_ros_container(){
    docker build -f ros.dockerfile -t $ros_docker_image_name .
}

# ------------------------------------------------------------------------------
pushd `pwd` > /dev/null 2>&1

build_gazebo_container
if [ $? -ne 0 ]; then
    echo "ERROR: could not build gazebo docker image"
    quit 1
fi

build_ros_container
if [ $? -ne 0 ]; then
    echo "ERROR: could not build ros docker image"
    quit 1
fi

quit_with_popd 0

