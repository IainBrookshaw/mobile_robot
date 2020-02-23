# Ningauble of the Seven Eyes

## Summary
Ningauble is a simple mobile robot that demonstrates:
- Containerized ROS and Gazebo
- Gazebo web server containerization and OS agnostic support
- Mobile Robot staples:
    - odometry
    - mapping
    - SLAM
    - obstacle avoidance
    - visualization

This is an exercise to demonstrate good-practice, neat coding and 
robot definition

### Scope

The Ningauble robot is a small mobile platform that __will__:
- use a  differential drive system
- move autonomously through a static environment
- avoid static obstacles in that environment
- maintain a map of the environment
- be as modular and clean in its architecture as possible
    - use low-level custom packages for:
        - servo motor control
        - path-planning
        - mapping
    - this is to demonstrate familiarity with these concepts
    - the ROS graph should be usable on a real robot, without explicitly drawing on Gazebo sim exploits

It __will not__:
- support manipulators
- support ackerman steering or skid-steering
- explicitly recognize dynamic obstacles (reactive avoidance "may" avoid these, but this is not first-class support)
- detect pitfalls and holes in the flat terrain
    - terrain is basically a 2-D plane with obstacles

--------
## Simulation Container Architecture

The Ningauble robot's containerization follows this overall architecture
``` 
                                                                   ||
                                                                   ||
+----------------------------+                +--------------+     ||
| Gazebo Server / ROS Master | -------------> | GZWeb Server |  --------> Host: Web Browser
+----------------------------+                +--------------+     ||
              |                                                    ||
              |                                                    ||
              |                                                    ||
+----------------------------+
|       Ning ROS Graph       |
+----------------------------+                        
```

- note that the Gazebo Server container could be swapped out for real hardware interfaces
- the use of the GZ web server "should" make this platform agnostic (hopefully!)

## Motor Control

## Perception

## Behaviors

## SLAM
### Odometry
### Sensor Kalman Filters

## Path Planning



---------
### Colophon

"Ningauble of the Seven Eyes" is a sorcerer created by the fantasy author 
Fritz Leiber in his acclaimed adventures of Fafherd and The Gray Mouser, 
The City of Lankhmar and the dreaming world of Nehwon.