#! /usr/bin/env bash
#
# Mobile Robot: Host System NVIDIA Install
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# Install Script for __Host System__ nvidia drivers
#

_minimum_kernel="4.15"

function check_host_nvidia_capabilities() {

    # Check that Nvidia hardware exists
    if lspci | grep -i -q nvidia | grep -q NVIDIA; then
        echo -e "$echo_error This machine does not have an Nvidia GPU:\n"
        echo lspci
        return -1
    fi
    echo -e "$echo_ok\t Nvidia Hardware present"

    # Check that this is x86-64 machine
    if cat /etc/*release | grep -q "x86_64"; then
        echo -e "$echo_error This is not an x86_64 architecture machine:\n"
        cat /etc/*release
        return -1
    fi
    echo -e "$echo_ok\t x86_64 Chipset Present"

    # Check that this is Ubuntu18.xx
    if ! cat /etc/*release | grep -q "Ubuntu 18"; then
        echo -e "$echo_error This is not a Ubuntu 18.xx Operating System:\n"
        cat /etc/*release
        return -1
    fi
    echo -e "$echo_ok\t OS is Ubuntu 18"

    # check the kernel version
    # todo: awk or sed this
    # v=`uname -r`
    # if [[ "$minimum_kernel" <= "$v" ]]; then
    #     echo -e "$echo_error Nvidia-docker2 needs a kernel version of $minimum_kernel or higher, have $v"
    #     return -1
    # fi
    # echo -e "$echo_ok\t Kernel version OK"
}


function install_nvidia_drivers_on_host() {

    if ! apt-get install -y linux-headers-$(uname -r)  > /dev/null 2>&1; then
        echo -e "$echo_error could not install the linux kernel headers"
        return -1
    fi

    echo -e "$echo_info\t pulling down Nvidia repo tools..."
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin > /dev/null 2>&1
    if ! mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600; then
        echo -e "$echo_error could not download repo pin"
        return -1
    fi
    echo -e "$echo_ok\t ...done"
    
    echo -e "$echo_info\t pulling down Nvidia keys..."
    apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub  > /dev/null 2>&1
    add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /"  > /dev/null 2>&1
    if [ "$?" -ne "0" ]; then 
        echo -e "$echo_error could not add nvidia repository"
        return -1
    fi
    echo -e "$echo_ok\t ...done"

    echo -e "$echo_info updating package manager..."
    apt-get update > /dev/null 2>&1
    echo -e "$echo_ok\t ...done"

    echo -e "$echo_info installing cuda..."
    if ! apt-get -y install cuda > /dev/null 2>&1 ; then
        echo -e "$echo_error could not install \"cuda\" package"
        return -1
    fi
    echo -e "$echo_ok\t ...done"

    # todo: echo this to ~/.bashrc??
    export PATH=/usr/local/cuda-10.1/bin:/usr/local/cuda-10.1/NsightCompute-2019.1${PATH:+:${PATH}}
}