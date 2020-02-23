# 
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c), 2020, All Rights Reserved
# MIT License
#
# Gazebo GZ web server

FROM  ubuntu-18.04
ARG ros_workspace_src="/ningauble_workspace/install"
ARG ros_workspace_dst="/ning-ros-workspace"
ENV GAZEBO_MODEL_PATH="${ros_workspace_dst}/share/models"

# Get All Ubuntu/Debian packages
RUN apt-get update && apt-get install -y \
    libjansson-dev \
    odejs \
    npm \
    libboost-dev \
    imagemagick \
    libtinyxml-dev \
    mercurial \
    cmake \
    build-essential

RUN mkdir -p ${ros_workspace_dst}
COPY ${ros_workspace_src} ${ros_workspace_dst}

# get all GZweb stuff
RUN hg clone https://bitbucket.org/osrf/gzweb \
    hg up gzweb_1.3.0 \
    source /usr/share/gazebo/setup.sh \
    ./deploy.sh -m

