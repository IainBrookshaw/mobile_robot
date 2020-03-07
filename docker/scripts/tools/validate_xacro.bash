#! /usr/bin/env bash
#
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c), 2020, All Rights Reserved
# MIT License
#
# Build Tool: Validate XACRO
# 
# The xacro macro language for robot description is notoriously difficult to 
# debug at gazebo runtime. This script confiures the call to the parser that
# is fast enough to fire at runtime
#
pushd `pwd` > /dev/null
cd $( cd $(dirname $0); pwd)
source ../common.bash

function source_all() {
    source /opt/ros/melodic/setup.bash
    source /ros_workspace/devel/setup.bash
}

function validate_xacro_file() {
    filepath=$1
    logdir=$2

    if [ ! -f $filepath ]; then
        logerr "unable to find xacro file \"$filepath\""
        return 1
    fi
    tmp_urdf=/tmp/tmp.urdf
    xacro $filepath > /tmp/tmp.urdf && check_urdf /tmp/tmp.urdf
}