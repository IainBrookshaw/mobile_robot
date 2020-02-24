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
name="ning-gzwebserver"
logdir="/tmp/ning/"
logfile=${logdir}/"gzwebserver.log"

mkdir -p $logdir

docker run \
    --rm \
    --name $name \
    --network host \
    ningauble:gzwebserver  &> $logfile

    