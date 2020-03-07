#! /usr/bin/env bash
#
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c) 2020, All Rights Reserved
# MIT License
#
# Todo: replace with docker config
#
pushd `pwd` > /dev/null
cd $( cd $(dirname $0); pwd)
source ../tools/common.bash

ros_workspace_path=$(cd "../../../ning_ros_workspace" && pwd)
ning_tools=$(cd "../../scripts/tools" && pwd)
loginf "using the directory $ros_workspace_path as source"
loginf "using the directiory $ning_tools as tool source"

function create_logdir() {
    path=$1
    loginf "creating logs at path \"$path\""
    mkdir -p $path/gzserver
    mkdir -p $path/gzweb
    mkdir -p $path/ros
    mkdir -p $path/docker
    logok "done"
}

function start_network() {
    name=$1
    loginf "creating network \"$name\""
    docker network create --driver bridge $name
}

function run_sim_server() {
    name=$1
    network=$2
    server_log_dir=$3
    docker_log_dir=$4
    gazebo_port=$5
    rospackage="ning_launch"
    roslaunchfile="ningauble_basic.launch"
    #
    user=$(id -u)
    group=$(id -g)
    #
    loginf "starting simulation backend container as \"$name\""
    loginf "         running as:    \"$user:$group\""
    loginf "         using network: \"$network\""
    loginf "         using port:    \"$gazebo_port\""
    loginf "         using docker log dir: \"$docker_log_dir\""
    loginf "         using gazebo log dir: \"$server_log_dir\""
    loginf "         using rospackage: \"$rospackage\""
    loginf "         using launchfile: \"$roslaunchfile\""

    docker run \
        --rm \
        -p $gazebo_port:$gazebo_port \
        --user $user:$group \
        --name $name \
        \
        --env ROSPACKAGE=$rospackage \
        --env LAUNCHFILE=$roslaunchfile \
        \
        --network $network \
        --volume=$server_log_dir:"/.gazebo" \
        --volume=${ros_workspace_path}:"/ros_workspace" \
        --volume=${ning_tools}:"/ning-tools" \
        \
        --volume="/etc/group:/etc/group:ro" \
        --volume="/etc/passwd:/etc/passwd:ro" \
        --volume="/etc/shadow:/etc/shadow:ro" \
        \
        ningauble:gazebo &> "$docker_log_dir/gzserver.log" &

    if [ $? -ne 0 ]; then
        logerr "backend startup failed"
        return 1
    fi
    return 0
}

function run_gzweb_server() {
    name=$1
    network=$2
    webserver_log_dir=$3
    gazebo_master_ip=$4
    gazebo_master_port=$5
    #
    

    loginf "starting gzweb server:"
    loginf "\tbackend container as: \"$name\""
    loginf "         logging to:    \"$webserver_log_dir\""
    loginf "         using network: \"$network\""
    loginf "         connecting to: \"$gazebo_master_ip:$gazebo_master_port\""

    docker run \
        --rm \
        -p 8080:8080 \
        --name $name \
        --network $network \
        --env=GAZEBO_MASTER_IP=$gazebo_master_ip \
        --env=GAZEBO_MASTER_URI=$gazebo_master_ip:$gazebo_master_port \
        ningauble:gzwebserver  &> "$webserver_log_dir/gzweb.log" &

    if [ $? -ne 0 ]; then
        logerr "backend startup failed"
        return 1
    fi
    return 0
}

function close_all() {
    sim_server=$1
    web_server=$2
    network=$3

    docker kill $sim_server $web_server
    docker network rm $network
}

# ----------------------------------------------------------------------------------------------------------------------
LOGDIR=/tmp/ning
NETWORK="ning-net"
WEB_SERVER_NAME="ning-gzweb"
SIM_SERVER_NAME="ning-gazebo"
GAZEBO_MASTER_PORT=11345
#
create_logdir $LOGDIR
start_network $NETWORK
echo

# Start the containers
run_sim_server $SIM_SERVER_NAME $NETWORK $LOGDIR/gzserver $LOGDIR/docker $GAZEBO_MASTER_PORT 
wait_for_container $SIM_SERVER_NAME
ip=$(get_container_ip $SIM_SERVER_NAME)

echo
run_gzweb_server $WEB_SERVER_NAME $NETWORK $LOGDIR/docker $ip $GAZEBO_MASTER_PORT
loginf "containers up, press <enter> to quit"
read -p ""
#
close_all $SIM_SERVER_NAME $WEB_SERVER_NAME $NETWORK
popd
