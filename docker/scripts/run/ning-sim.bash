#! /usr/bin/env bash
#
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c) 2020, All Rights Reserved
# MIT License
#
pushd `pwd` > /dev/null
cd $( cd $(dirname $0); pwd)
source ../common.bash

function create_logdir() {
    path=$1
    loginf "crating logs at path \"$path\""
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
    loginf "starting simulation backend"

    docker run \
        --rm \
        --detach \
        -p 11345:11345 \
        --name $name \
        --network $network \
        --volume=$server_log_dir:"/.gazebo" \
        ningauble:sim-backend "--paused" &> "$docker_log_dir/gzserver.log"

    if [ $? -ne 0 ]; then
        logerr "startup failed"
        return 1
    fi
    return 0
}

function run_gzweb_server() {
    name=$1
    network=$2
    webserver_log_dir=$3
    master_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ning-sim)
    loginf "starting gzweb server, connecting to $master_ip"

    docker run \
        --rm \
        --detach \
        -p 8080:8080 \
        --name $name \
        --network $network \
        --env=GAZEBO_MASTER_IP=$master_ip \
        ningauble:gzwebserver  &> "$webserver_log_dir/gzweb.log"

    if [ $? -ne 0 ]; then
        logerr "startup failed"
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
SIM_SERVER_NAME="ning-sim"
#
create_logdir $LOGDIR
start_network $NETWORK
run_sim_server $SIM_SERVER_NAME $NETWORK $LOGDIR/gzserver $LOGDIR/docker
run_gzweb_server $WEB_SERVER_NAME $NETWORK $LOGDIR/docker
#
loginf "containers up, press <enter> to quit"
read -p ""
#
close_all $SIM_SERVER_NAME $WEB_SERVER_NAME $NETWORK
popd
