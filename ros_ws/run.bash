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

    echo "run.bash: stopping gazebo container"
    docker stop $gazebo_run_container_name > /dev/null 2>&1
    docker rm   $gazebo_run_container_name > /dev/null 2>&1

    echo "run.bash: stopping ros container"
    docker stop $ros_run_container_name > /dev/null 2>&1
    docker rm   $ros_run_container_name > /dev/null 2>&1
    
    popd > /dev/null 2>&1
    exit $1
}

function run_gazebo(){

    echo "run_gazebo: Standing Up Gazebo Plugins"
    docker run  \
        --name $gazebo_run_container_name \
        --env RUN_MODE="run" \
        --volume $gazebo_src_code_dir:$gazebo_volume \
        --volume $run_scripts_dir:$run_scripts_volume \
        --env="DISPLAY" \
        --env="QT_X11_NO_MITSHM=1" \
        --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
        $gazebo_img_name > /dev/null 2>&1

    echo "run_gazebo: Connecting the Gazebo container to the hosts X-Server"
    export containerId=$(docker ps -l -q)
    xhost +local:`docker inspect --format='{{ .Config.Hostname }}' $containerId`
    docker start $containerId

    return $?
}

function run_ros(){
    echo "Running the ROS Architecture"
    docker run \
        --name $ros_run_container_name \ 
        --volume ../ros_ws \
        $ros_img_name
    return 0
}

# ----------------------------------------------------------------------------------------------------------------------
# MAIN

pushd `pwd`
cd `dirname "$0"`

echo "run.bash: running gazebo container"
run_gazebo > /dev/null 2>&1 &

echo "run.bash: running ros container"
run_ros  > /dev/null 2>&1 &

read -p "Press enter to stop both containers..."
echo "Run Finished, closing containers"
quit 0