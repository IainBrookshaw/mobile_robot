#! /bin/bash
#
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c) 2020, All Rights Reserved
# MIT License
#
pushd `pwd` > /dev/null
cd $( cd $(dirname $0); pwd)

function create_logdir() {
    path=$1
    mkdir -p $path/gzserver
    mkdir -p $path/gzweb
    mkdir -p $path/ros
    mkdir -p $path/docker
}

function start_network() {
    name=$1
    docker network create --driver bridge $name
}

function run_sim_server() {
    name=$1
    network=$2
    server_log_dir=$3
    docker_log_dir=$4

    docker run \
        --rm \
        --detach \
        -p 11345:11345 \
        --name $name \
        --network $network \
        --volume=$server_log_dir:"/.gazebo" \
        ningauble:sim-backend &> "$docker_log_dir/gzserver.log"
}

function run_gzweb_server() {
    name=$1
    network=$2
    webserver_log_dir=$3

    docker run \
        --rm \
        --detach \
        -p 8080:8080 \
        --name $name \
        --network $network \
        ningauble:gzwebserver  &> "$webserver_log_dir/gzweb.log"
}

function close_all() {
    sim_server=$1
    web_server=$2
    network=$3

    docker kill $sim_server $web_server
    docker network rm $network
}

# ------------------------------------------------------------------------------
LOGDIR=/tmp/ning
NETWORK="ning-net"
WEB_SERVER_NAME="ning-gzweb"
SIM_SERVER_NAME="ning-sim"

create_logdir $LOGDIR
start_network $NETWORK
run_sim_server $SIM_SERVER_NAME $NETWORK $LOGDIR/gzserver $LOGDIR/docker
run_gzweb_server $WEB_SERVER_NAME $NETWORK $LOGDIR/docker

read -p "press <enter> to quit"

close_all $SIM_SERVER_NAME $WEB_SERVER_NAME $NETWORK
popd
