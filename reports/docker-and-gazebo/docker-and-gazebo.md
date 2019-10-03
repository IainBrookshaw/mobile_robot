# Docker and Gazebo

- to get full docker image for ROS:
    - `docker pull osrf/ros:kinetic-desktop-full-xenial`
    - or:
        - `docker pull osrf/ros:ros-distro-name-desktop-full-ubuntu-distro-name`
    - note that `docker pull x` automatically puts the `:latest` tag of package `x`
    - in docker world, this is analogous to the git `master` or `release` branch

- to get full (with graphics) docker image for Gazebo:
    - `docker pull osrf/gazebo:gzserverX`
    - osrf gazebo has several tags
        - mostly different gzweb versions


- it is also possible to allow the docker container to access the 
  (Nvida drivers)[http://wiki.ros.org/docker/Tutorials/Hardware%20Acceleration]

## Docker X-Server Connection

- simplest method: connect to the X11 Unix socket:
```bash
docker run -it \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    osrf/ros:indigo-desktop-full \
    rqt
export containerId=$(docker ps -l -q)
```
- `--env="QT_X11_NO_MITSHM=1"` forces Qt to behave properly
- this is what [1](https://bisraelsen.github.io/2017/docker/) did
- it is __not__ secure

- this approach:
    - makes the container's processes interactive (`-it`)
    - forwards the `DISPLAY` env var to the container
    - mounts a volume for the X11 Unix Socket
    - This approach will __fail__ with `No protocol specified` error

- to make it work:
    - __lazy solution:__ run `xhost +local:root` on host before running the the container.
        - this is a __horible__ solution, it relies on opening the permissions of the XServer, which makes your XServer vulnerable

    - __better solutions:__
        1. run the lazy solution and then, after the simulation is closed, run `xhost -local:root`, which at least re-sets the XServer
        2. Open the XServer to the container __only__
            - run: (note the bash back-ticks)
            ```bash
            xhost +local:`docker inspect --format='{{ .Config.Hostname }}' $containerId`
            docker start $containerId
            ```
            - This adds the container's name to the local list of permitted names

            



--------
## References
- [Official OSRF Docker](https://hub.docker.com/u/osrf/)
- [1](https://bisraelsen.github.io/2017/docker/) 