# Mobile Robot: Robot Architecture RUN Dockerfile
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# to build: docker build -t myimagename .     # default 'Dockerfile'
#           docker build -f FirstDockerfile . # custom dockerfile
#
FROM osrf/ros:melodic-desktop-bionic

# TODO: INSTALL BUILD ARTIFACTS HERE

CMD scripts/run-robot.bash

