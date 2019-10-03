#!/usr/bin/env python
"""
Mobile Robot: Hardware Motor Comms Node
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""
import rospy

# Because we are going from the real-to simulated world, we __cannot__ just use the system clock
# need to use the simulated clock
import mobilerobot_time as time


from std_msgs.msg import String
# TODO: Other messages here


class NoMicrocontrollerError(Exception):
    """raised if no communications to microcontroller exists"""
    pass


class CommsError(Exception):
    """something wrong in the packet passed from the motor microcontroller"""
    pass


class MotorState:
    """
    Current state of the motors, both actual and commanded
    """

    def __init__(self):
        self.timestamp = -1.0
        self.left_motor_speed = 0.0
        self.right_motor_speed = 0.0

    def dt(self):
        return time.time() - self.timestamp

    def updated_since(self, last_seen):
        return last_seen < self.timestamp

# ----------------------------------------------------------------------------------------------------------------------
# Global State


_ros_motor_command = MotorState()
_micro_motor_state = MotorState()

# ----------------------------------------------------------------------------------------------------------------------
# ROS Publication and Subscription


def _publish_encoder_state(pub, state):
    """
    Publish the motor state to the greater ROS system
    """
    # todo: marshal the message !!!
    encoder_msg = None
    pub.publish(state)


def _ros_motor_command_cb(cmd):
    """
    handles the ROS motor command subscription
    """
    pass

# ----------------------------------------------------------------------------------------------------------------------
# Microcontroller Communications


def _send_motor_command(cmd):
    """
    send a motor command down the comms line to the motor hardware
    """
    pass


def _motors_all_stop():
    """
    Send Emergency STOP to motors, something has gone wrong
    """
    pass


def _register_micro_controller_callback(cb):
    """
    connects to the hardware line for micro-controller communications
    """
    pass


def _motor_mico_controller_cb():
    """
    callback for message from the motor micro-controller
    """
    pass


# ----------------------------------------------------------------------------------------------------------------------
# Node Main Program
#
def _motor_controller_hw_node():
    """
    This is the main ROS node for real-world motor control.
    """

    # ROS boilerplate
    rospy.init_node('motor_controller_hw', anonymous=True)
    rate = rospy.Rate(20)  # 10hz # TODO: make this an arg

    # todo: correct message type
    encoder_pub = rospy.Publisher("encoders", String, queue_size=10)

    last_micro_state_stamp = time.time()
    last_ros_state_stamp = time.time()

    # Node Main Loop
    while not rospy.is_shutdown():

        # check if any new motor commands have come in
        if _ros_motor_command.updated_since(last_ros_state_stamp):
            _send_motor_command(_ros_motor_command)
            last_ros_state_stamp = _ros_motor_command.timestamp

        # check if any new micro-controller states have come back
        if _micro_motor_state.updated_since(last_micro_state_stamp):
            _publish_encoder_state(encoder_pub, _micro_motor_state)
            last_micro_state_stamp = _micro_motor_state.timestamp

        # ... and cycle the node
        rate.sleep()

# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    try:
        _motor_controller_hw_node()
    except rospy.ROSInterruptException:
        pass
