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
source common.bash

function source_all() {
    declare -a sources
    sources[0]="/opt/ros/melodic/setup.bash"
    sources[1]="/ros_workspace/devel/setup.bash"

    for f in "${sources[@]}"; do
        if [[ ! -f $f ]]; then
            logerr "Cannot source ROS setup.bash at \"$f\""
            return 1
        fi
        source $f
    done
    return 0
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
    if [ $? -ne 0 ]; then
        logerr "xacro validation failed"
        return 1
    fi
}


# ----------------------------------------------------------------------------------------------------------------------
# Main Program

loginf "about to validate XACRO files prior to Gazebo load"
if ! source_all; then exit 1; fi
if ! validate_xacro_file "/ros_workspace/src/ning_urdf/urdf/ningauble.xacro"; then exit 1; fi
logok "done, all xacro's pass validation"
exit 0