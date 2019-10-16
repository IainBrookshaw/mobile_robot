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

_this_dir="$( cd "$(dirname "$0")" ; pwd -P )"
pushd `pwd` > /dev/null 2>&1
cd $_this_dir

source scripts/mobile-robot.bash


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
    echo -e "\tbuild_ros: Building ROS Architecture"
    # docker run \
    #     --name build-ros \ 
    #     --volume ../ros_ws \
    #     $ros_img_name
    return 0
}

# ----------------------------------------------------------------------------------------------------------------------
# MAIN

build_flag="build"
if [ "$1" == "clean" ]; then
    build_flag="build-clean"
fi

build_gazebo $build_flag
if [ $? -ne 0 ]; then
    echo "ERROR: gazebo build failed!"
    quit 1
fi
echo

# build_ros
# if [ $? -ne 0 ]; then
#     echo "ERROR: ros build failed"
#     quit 1
# fi

echo "Builds Complete"
quit 0