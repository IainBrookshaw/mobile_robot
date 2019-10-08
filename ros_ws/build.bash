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

# ----------------------------------------------------------------------------------------------------------------------
# PATHS

# directories/volume mapping
gazebo_src_code_dir="`pwd`/gazebo"
gazebo_volume="/gazebo"
#
build_scripts_dir="`pwd`/scripts"
build_scripts_volume="/scripts"
#
ros_src="`pwd`/src"
ros_volume="/ros"

# container names
gazebo_img_name="mobile-robot-gazebo:latest"
gazebo_build_container_name="mobile-robot-build-gazebo"

ros_img_name="mobile-robot-ros:latest"
ros_build_container_name="mobile-robot-build-ros"

# ----------------------------------------------------------------------------------------------------------------------
# FUNCTIONS

function quit(){
    docker rm $gazebo_build_container_name > /dev/null 2>&1
    docker rm $ros_build_container_name > /dev/null 2>&1
    popd > /dev/null 2>&1
    exit $1
}

function build_gazebo(){

    echo "Building Gazebo Plugins:"
    docker run \
        --name $gazebo_build_container_name \
        -v $gazebo_src_code_dir:$gazebo_volume \
        -v $build_scripts_dir:$build_scripts_volume \
        --env RUN_MODE="build" \
        $gazebo_img_name

    return $?
}

function build_ros(){
    echo "Building ROS Architecture"
    # docker run \
    #     --name build-ros \ 
    #     --volume ../ros_ws \
    #     $ros_img_name
    return 0
}

# ----------------------------------------------------------------------------------------------------------------------
# MAIN

pushd `pwd`
cd `dirname "$0"`

build_gazebo
if [ $? -ne 0 ]; then
    echo "ERROR: gazebo build failed!"
    quit 1
fi
echo

build_ros
if [ $? -ne 0 ]; then
    echo "ERROR: ros build failed"
    quit 1
fi

echo "Builds Complete"
quit 0