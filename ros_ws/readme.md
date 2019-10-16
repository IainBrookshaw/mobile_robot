# Mobile Robot (ROS and Gazebo)

## Install Docker

We use Docker containers for both the building and running of the Gazebo 
simulator and the ROS architecture. Thus you do not need to install ROS or 
Gazebo on your host machine

To setup for build simply install Docker as follows:

- __Ubuntu:__ 
    - [1](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
    - [2](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

- __MacOSX:__
    - [1](https://docs.docker.com/docker-for-mac/install/)

### Containers

## Build the Docker Images
At this time, we do not have the images hosted on DockerHub. You will have to 
build the container images locally (sorry).

This has been nicely scripted for you:
```bash
./build-images.bash
```

## Build the Gazebo Plugins and the ROS Architecture
```bash
./build.bash
```
If errors occur in the build, this script will cat them
to the command line as normal (although you do lose syntax
highlighting)

## Run the system
```bash
./run.bash
```
This will kill the containers on exit, but this takes some time for Gazebo

## Notes
- The chain of scripts for building is cumbersome, and should be docker-compose-erized, but at this time, it is convenient to have development done using scripts