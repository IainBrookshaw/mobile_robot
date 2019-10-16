# Mobile Robot: Run ALL the robot
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

function quit(){

    echo -e "\trun.bash: stopping gazebo container"
    docker stop $gazebo_docker_run_container_name > /dev/null 2>&1
    docker rm   $gazebo_docker_run_container_name > /dev/null 2>&1

    echo -e "\trun.bash: stopping ros container"
    docker stop $ros_docker_run_container_name > /dev/null 2>&1
    docker rm   $ros_docker_run_container_name > /dev/null 2>&1
    
    quit_with_popd 0
}

function run_gazebo(){

    echo -e "\trun_gazebo: Standing Up Gazebo Simulator"

    docker run \
        --name $gazebo_docker_run_container_name \
        --volume $gazebo_src_volume_host_path:$gazebo_src_volume_name \
        --volume $gazebo_scripts_volume_host_path:$gazebo_scripts_volume_name \
        --env RUN_MODE="run" \
        --env="DISPLAY" \
        --env="QT_X11_NO_MITSHM=1" \
        --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
        $gazebo_docker_image_name 
        
    #> /dev/null 2>&1
    if [ $? -ne 0 ]; then 
        echo "ERROR: could not run the gazebo docker image"
        quit 1
    fi

    echo -e "\trun_gazebo: Connecting the Gazebo container to the hosts X-Server"
    export containerId=$(docker ps -l -q)
    xhost +local:`docker inspect --format='{{ .Config.Hostname }}' $containerId`
    docker start $containerId

    return $?
}

function run_ros(){
    echo -e "\trun_ros: Running the ROS Architecture"
    # docker run \
    #     --name $ros_run_container_name \ 
    #     --volume ../ros_ws \
    #     $ros_img_name
    # return 0
}

# ----------------------------------------------------------------------------------------------------------------------
# MAIN

echo "run.bash: running gazebo container"
run_gazebo #> /dev/null 2>&1 &
if [ $? -ne 0 ]; then
    echo "ERROR: could not start gazebo docker container!"
    quit 1
fi

echo "run.bash: running ros container"
run_ros  > /dev/null 2>&1 &
if [ $? -ne 0 ]; then
    echo "ERROR: could not start ROS docker container!"
    quit 1
fi

echo "Both ROS and Gazebo containers started and running."
read -p "Press <any key> to stop both containers: "
echo "Run Finished, closing both ROS and Gazebo containers..."
quit 0