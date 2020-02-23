#! /bin/bash
#
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c), 2020, All Rights Reserved
# MIT License
#
# Dockerfile Compilation

pushd `pwd` > /dev/null
cd $( cd $(dirname $0); pwd)
context="../.."

docker build \
    --file ${context}/dockerfiles/ning-sim.dockerfile \
    --tag "ningauble:sim-backend" \
    $context

docker build \
    --file ${context}/dockerfiles/ning-sim-webserver.dockerfile \
    --tag "ningauble:gzwebserver" \
    $context