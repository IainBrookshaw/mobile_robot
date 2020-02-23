#! /bin/bash 
#
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c), 2020, All Rights Reserved
# MIT License
#
# Gazebo web server

pushd `pwd` > /dev/null
cd $( cd $(dirname $0); pwd)
context="../.."

docker run --rm \
    --name "ning-gzwebserver" \
    --network host \
    