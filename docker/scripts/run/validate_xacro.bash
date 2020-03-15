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


function check_path (){
    if [ ! -f $1 ]; then
        logerr "Xacro file \"$1\" does not exist"
        return 1
    fi
    return 0
}

function validate_xacro() {
    
    check_urdf <(xacro --inorder $1)
    if [ $? -ne 0 ]; then
        logerr "Xacro fails validation"
        return 1
    fi
    return 0
}

# ------------------------------------------------------------------------------

function run_in_docker() {
    loginf "checking xacro file path"
    if ! check_path $1; then 
        exit 1
    fi
    logok "xacro file path ok"

    loginf "validating xacro"
    if ! validate_xacro $1; then
        exit 1
    fi
    logok "xacro passes validation"
    exit 0
}

# ------------------------------------------------------------------------------

docker run \
    --name "validate-xacro" \
    --volume "/ning_ros_workspace":"../../../ning_ros_workspace" \
    ningauble:gazebo "/bin/bash "