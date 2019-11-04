#! /usr/bin/env bash
#
# Mobile Robot: Host System NVIDIA-Docker2 Install
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# Install Script for __Host System__ nvidia Docker Plugin
#
function install_nvidia_docker2_on_host(){

    echo -e "$echo_info:\t adding nvidia-docker key..."
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.dnvidia-docker.list
    if [ $? -ne "0" ]; then
        echo -e "$echo_error could not at nvidia-docker key"
        return -1
    fi
    echo -e "$echo_ok\t ...done"
    
    echo -e "$echo_info\t installing nvidia-docker2..."
    apt-get update
    apt-get install nvidia-docker2
    if [ $? -ne "0" ]; then
        echo -e "$echo_error could not install package \"nvidia-docker2\""
        return -1
    fi
    echo -e "$echo_ok\t ...done"
    return 0
}

function test_nvidia_docker_on_host() {
    out="/tmp/nvidia-docker-test.txt"
    docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi > $out
    if [ $? -ne "0" ]; then
        echo -e "$echo_error Could not run Nvidia test Docker container:"
        echo
        cat $out
        return -1
    fi
    return 0
}