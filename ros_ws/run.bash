# Mobile Robot: Run ALL the robot
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# Running this script will start up both the gazebo simulation and ROS architecture
# containers 
#
# For this script to work, you must run:
#   - `build-docker-images.bash`
#   - `build.bash`

# ----------------------------------------------------------------------------------------------------------------------
# PATHS

# directories/volume mapping
gazebo_src_code_dir="`pwd`/gazebo"
gazebo_volume="/gazebo"
#
run_scripts_dir="`pwd`/scripts"
run_scripts_volume="/scripts"
#
ros_src="`pwd`/src"
ros_volume="/ros"

# container names
gazebo_img_name="mobile-robot-gazebo:latest"
gazebo_run_container_name="mobile-robot-run-gazebo"

ros_img_name="mobile-robot-ros:latest"
ros_run_container_name="mobile-robot-run-ros"

# ----------------------------------------------------------------------------------------------------------------------
# FUNCTIONS

function quit(){
    docker rm $gazebo_run_container_name > /dev/null 2>&1
    docker rm $ros_run_container_name > /dev/null 2>&1
    popd > /dev/null 2>&1
    exit $1
}

function run_gazebo(){

    echo "Standing Up Gazebo Plugins"

    docker run \
        --name $gazebo_run_container_name \
        -v $gazebo_src_code_dir:$gazebo_volume \
        -v $run_scripts_dir:$run_scripts_volume \
        --env RUN_MODE="run" \
        $gazebo_img_name

    if [ $? -ne 0 ]; then
        return 1
    fi

    echo "Connecting the Gazebo container to the hosts X-Server"
    export containerId=$(docker ps -l -q)
    xhost +local:`docker inspect --format='' $containerId`
    docker start $containerId

    return $?
}

function run_ros(){
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

run_gazebo
if [ $? -ne 0 ]; then
    echo "ERROR: gazebo run failed!"
    quit 1
fi
echo

run_ros
if [ $? -ne 0 ]; then
    echo "ERROR: ros run failed"
    quit 1
fi

echo "Builds Complete"
quit 0