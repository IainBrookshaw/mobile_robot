#! /usr/bin/env bash
#
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c), 2020, All Rights Reserved
# MIT License
#
# Dockerfile Compilation

pushd `pwd` > /dev/null
cd $( cd $(dirname $0); pwd)

source ../common.bash
context="../.."

function build_sim_server() {
    loginf "building sim-backend docker image..."

    docker build \
        --file ${context}/dockerfiles/gzserver.dockerfile \
        --tag "ningauble:gazebo" \
        $context
    if [ $? -ne 0 ]; then
        logerr "unable to build sim-backend"
        return 1
    fi
    logok "done"
    return 0
}

function build_gzwebserver() {
    loginf "building gzwebserver docker image..."

    docker build \
        --file ${context}/dockerfiles/gzweb.dockerfile \
        --tag "ningauble:gzwebserver" \
        $context
    if [ $? -ne 0 ]; then
        logerr "unable to build gzwebserver"
        return 1
    fi
    logok "done"
    return 0
}

function build_ros_runner() {
    loginf "building ros-runner docker image..."

    docker build \
        --file ${context}/dockerfiles/ros_runner.dockerfile \
        --tag "ningauble:ros_runner" \
        $context
    if [ $? -ne 0 ]; then
        logerr "unable to build ros_runner"
        return 1
    fi
    logok "done"
    return 0
}

# ------------------------------------------------------------------------------
# Main Program

if ! build_sim_server; then
    exit 1
fi
if ! build_gzwebserver; then
    exit 1
fi
if ! build_ros_runner; then
    exit 1
fi