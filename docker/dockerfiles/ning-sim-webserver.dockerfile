# 
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c), 2020, All Rights Reserved
# MIT License
#
# Gazebo GZ web server

FROM ubuntu:bionic

ARG ros_workspace_src="/ningauble_workspace/install"
ARG ros_workspace_dst="/ning-ros-workspace"
ENV GAZEBO_MODEL_PATH="${ros_workspace_dst}/share/models"

# install gazebo
RUN apt-get update && apt-get install -y \
    gazebo9 \
    libgazebo9-dev

# Node and others needed to build webserver
RUN apt-get update && apt-get install -y \
    libjansson-dev \
    pkg-config \
    libssl1.0-dev \
    nodejs-dev \
    node-gyp \
    nodejs \
    npm \
    libboost-dev \
    imagemagick \
    libtinyxml-dev \
    mercurial \
    cmake \
    build-essential

# install NPM
RUN apt-get install -y \
    git-core \
    curl \
    build-essential \
    openssl \
    libssl-dev && \
    curl -L https://npmjs.org/install.sh | sh

RUN mkdir -p ${ros_workspace_dst}
# COPY ${ros_workspace_src} ${ros_workspace_dst}

# get all GZweb stuff
RUN hg clone https://bitbucket.org/osrf/gzweb
WORKDIR gzweb
RUN hg up master && \
    npm run deploy
# RUN ./deploy.sh -m

