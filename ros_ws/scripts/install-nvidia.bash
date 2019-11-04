#! /usr/bin/env bash
#
# Mobile Robot: Host System NVIDIA Install
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# This is an install script for NVIDIA driver and NVIDIA-Docker setup on the 
# __HOST__ machine
#
# ----------------------------------------------------------------------------------------------------------------------
#
_this_dir="$( cd "$(dirname "$0")" ; pwd -P )"
pushd `pwd` > /dev/null 2>&1
cd $_this_dir

# Nvidia Install Functions
source "mobile-robot.bash"
source "nvidia_install/driver-install.bash"
source "nvidia_install/docker-plugin-install.bash"

echo -e "$B
 +-------------------------------------------------------------------------------+
 |  Mobile Robot Simulation                                                      |
 |                                                                               |
 |  Host NVIDIA Driver Install & Setup                                           |
 +-------------------------------------------------------------------------------+ $rs
"



# is root?
if [ "$EUID" -ne 0 ]; then 
    echo -e "$echo_error Please run as root"
    quit_with_popd -1
fi

echo -e "$echo_info Checking host system for Nvidia Capability..."
if ! check_host_nvidia_capabilities; then
    quit_with_popd 1
fi
echo -e "$echo_ok ...done"

echo -e "$echo_info Installing Nvidia System drivers on Host..."
if ! install_nvidia_drivers_on_host; then
    quit_with_popd 1
fi
echo -e "$echo_ok ...done"

echo -e "$echo_info Installing Nvidia-Docker2 drivers on Host..."
if ! install_nvidia_docker2_on_host > /dev/null 2>&1; then
    quit_with_popd 1
fi
echo -e "$echo_ok ...done"

# echo -e "$echo_info Restarting Docker Daemon..."
# if ! reset_host_for_nvidia_docker2; then
#     quit_with_popd 1
# fi
# echo -e "$echo_ok ...done"

echo -e "$echo_info running test Nvidia Docker container (this may take some time)..."
if ! test_nvidia_docker_on_host; then
    quit_with_popd 1
fi
echo -e "$echo_ok ...done"
