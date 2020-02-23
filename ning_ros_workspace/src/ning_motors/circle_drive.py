#! /usr/bin/env python
#
# Iain Brookshaw
# Copyright (c), 2019. All Rights Reserved
# MIT License
#
# Simple script to drive the robot in circles
# TODO: expand this into a proper motor controller -- it's a demo at the moment and very hacky
#
import numpy as np

import rospy
from std_msgs.msg import Float64
from rosgraph_msgs.msg import Clock


class CircleDriver:

    def __init__(self):
        self._left_motor_cmd_topic = "/mobile_robot/left_motor_position_controller/command"
        self._right_motor_cmd_topic = "/mobile_robot/right_motor_position_controller/command"

        self._final_wheel_velocity = np.pi  # one rotation every second
        self._max_wheel_accel = np.pi/24.0  # rad/sec/sec

        self._current_time = 0.0
        self._last_speed_update_time = 0.0
        self._last_pose_update_time = 0.0
        self._current_left_speed = 0.0
        self._current_right_speed = 0.0
        self._current_left_pose = 0.0
        self._current_right_pose = 0.0

    def clock_calback(self, data):
        self._current_time = float(data.clock.secs) + \
            (1e-9)*float(data.clock.nsecs)

    def now(self):
        return self._current_time

    def update_speeds(self, target_speed):
        """ for now right just goes backwards """
        dt = self.now() - self._last_speed_update_time
        if dt < 0.00001:
            return

        if self._current_left_speed < self._final_wheel_velocity:
            self._current_left_speed += dt * self._max_wheel_accel

        if self._current_right_speed < self._final_wheel_velocity:
            self._current_right_speed += dt * self._max_wheel_accel

        self._last_speed_update_time = self.now()

    def update_poses(self):
        dt = self.now() - self._last_pose_update_time
        if dt < 0.00001:
            return

        self._current_left_pose += self._current_left_speed * dt
        self._current_right_pose += 0.8*self._current_right_speed * dt

        self._last_pose_update_time = self.now()

    def run(self):
        """
        This function publishes to the robot's wheel motors in an attempt to drive
        it around in circles for demonstration/test purposes
        """
        left_motor_pub = rospy.Publisher(
            self._left_motor_cmd_topic, Float64, queue_size=10
        )
        right_motor_pub = rospy.Publisher(
            self._right_motor_cmd_topic, Float64, queue_size=10
        )
        rospy.Subscriber("/clock", Clock, self.clock_calback)

        rospy.init_node("circle_motor_driver", anonymous=True)
        rate = rospy.Rate(10)  # hz

        while not rospy.is_shutdown():
            self.update_speeds(self._final_wheel_velocity)
            self.update_poses()
            #
            left_motor_pub.publish(Float64(self._current_left_pose))
            right_motor_pub.publish(Float64(self._current_right_pose))
            rate.sleep()

# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    try:
        circle_driver = CircleDriver()
        circle_driver.run()

    except rospy.ROSInterruptException:
        pass
    except Exception as e:
        rospy.logerr("Exception in circle driver: {}".format(e))
