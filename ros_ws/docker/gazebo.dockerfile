# Mobile Robot: Robot Architecture Dockerfile
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# to build: docker build -t myimagename .     # default 'Dockerfile'
#           docker build -f FirstDockerfile . # custom dockerfile
#
FROM osrf/ros:melodic-desktop-bionic

RUN scripts/build_install_robot_arch.bash

CMD scripts/run_robot_arch.bash

