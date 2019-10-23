# Mobile Robot (ROS and Gazebo)

This is a simple illustrative example of a mobile robot. It's main controller,
behaviors, planners and other robot parts have been built using ROS and run 
in a self-contained Docker image, while a Gazebo simulator can be launched 
in another.

The purpose of this robot is to illustrate how to do this task (which is 
somewhat involved) and provide an example of basic mobile robot features

## Quickstart

To run the simulated robot, do the following:

1. install docker

2. build the docker images (this will take quite a while)
    - `build-images.bash`

3. build all the ROS and Gazebo systems
    - `build.bash`

Once all these build-install steps have been completed, you may run the robot/simulation as follows:

`run.bash`

It may take some time for the Gazebo to start up on you computer

__Note:__
- you do not need to install anything on the host machine (other than Docker)
- Gazebo and ROS are fully containerized
- Gazebo visualizations may only work on a Linux host machine (they need and assume an XServer)
    - visualizations on any host platform other than Ubuntu18 are untested

------------------------------------------------------------------------------------------------------------------------

## Install Docker

We use Docker containers for both the building and running of the Gazebo 
simulator and the ROS architecture. Thus you do not need to install ROS or 
Gazebo on your host machine

To setup for build simply install Docker as follows:

- __Ubuntu:__ 
    - [Tutorials](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
    - [Ubuntu Install](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

## Notes
- The chain of scripts for building is cumbersome, and should be docker-compose-erized, but at this time, it is convenient to have development done using scripts