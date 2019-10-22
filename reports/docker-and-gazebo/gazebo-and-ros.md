# Gazebo and ROS

__ROS:__ Melodic

__Gazebo:__ 9.*

## Connecting ROS to Stand Alone Gazebo

- can use the `gazebo_ros_pkgs`
- supports _stand alone_ gazebo, with no ROS bindings of it's own
    - I like this approach, as it enforces a nice separation
- builds with `catkin`
- tries to treat `urdf == sdf`
    - this is probably going to be a pain regardless
- this is the `ros_control` path for controllers

## Minimal Files

### CMake
```cmake
cmake_minimum_required(VERSION 2.8.3)
project(YOURROBOT_gazebo_plugins)

find_package(catkin REQUIRED COMPONENTS
  gazebo_ros
)

# Depend on system install of Gazebo
find_package(gazebo REQUIRED)

include_directories(include ${catkin_INCLUDE_DIRS} ${GAZEBO_INCLUDE_DIRS} ${SDFormat_INCLUDE_DIRS})

# Build whatever you need here
add_library(...) # TODO

catkin_package(
    DEPENDS
      gazebo_ros
    CATKIN_DEPENDS
    INCLUDE_DIRS
    LIBRARIES
)
```
### `package.xml` (ROS)
```xml
<build_depend>gazebo_ros</build_depend>
<run_depend>gazebo_ros</run_depend>
```


## Launch

- to run gazebo in this situation:
```bash
    rosrun gazebo_ros gazebo # launches both the client and gui
```

- You can use `roslaunch` to run gazebo and spawn robots
    - see [here](http://gazebosim.org/tutorials?tut=ros_roslaunch&cat=connect_ros) for args
    - important args:
        - `paused` -- launch simulation paused
        - `use_sim_time` -- __IMPORTANT__ make ROS use the simulated time, not the system time
        

----------

# Sources
- [1](http://gazebosim.org/tutorials?tut=ros_overview)