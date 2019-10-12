/**
 * Mobile Robot: Differential Drive Plugin
 * Iain Brookshaw
 * Copyright (c), 2019. All Rights Reserved
 * MIT License
 *
 * http://gazebosim.org/tutorials?tut=ros_gzplugins
 */
#include <ros_ws/ros.h>
#include <gazebo/common/Plugin.hh>

#include <unistd.h>
#include <ctime>

#define AWAIT_ROS_TIMEOUT 5  // seconds

namespace gazebo {

/**
 * \brief A model of a simple DC motor and gearbox.
 */
class MotorModel {
 private:
  double current_rotation_velocity = 0.0;  // radians/sec
  double target_rotation_velocity = 0.0;   // radians/sec
  double timestamp = 0.0;                  // seconds
  double power_state = 0.0;                // -1.0 -> 1.0

 public:
  MotorModel();

  double get_rotation_velocity() { return this->rotation_velocity; }

  void set_motor_power(double power, double timestamp) {
    this->power_state = power;
    this->timestamp = timestamp;
  }

  /**
   * \brief computes the current rotational velocity at this time
   * \param now -- current timestamp in seconds
   *
   * Currently this is linear with respect to time only.
   * todo: add a more sophisticated motor model.
   */
  double update_rotation_velocity(double now) {}

};  // end of MotorModel

// ---------------------------------------------------------------------------------------------------------------------

/**
 * /brief motors and encoders for a differential drive robot in gazebo
 */
class DDrivePlugin : public ModelPlugin {
 private:
  physics::ModelPtr model;
  event::ConnectionPtr updateConnection;

  // command timestamps

  // Motor Control Parameters
  double left_motor_command = 0.0;   // -1.0 to 1.0
  double right_motor_command = 0.0;  // -1.0 to 1.0
  //
  //   double left_motor_rot_velocity = 0.0;   // radians
  //   double right_motor_rot_velocity = 0.0;  // radians
  //
  double left_motor_encoder = 0.0;   // rad/sec
  double right_motor_encoder = 0.0;  // rad/sec

 public:
  DDrivePlugin() : ModelPlugin() {
    // constructor: nothing here for now
  }

  /**
   * \brief Run by the Gazebo simulator on loading the simulation
   */
  void Load(physics::WorldPtr _world, std::ElementPtr _sdf) {
    // Make sure the ROS node for Gazebo has already been initialized
    if (this->wait_for_ros()) {
      ROS_FATAL_STREAM(
          "A ROS node for Gazebo has not been initialized, unable to load "
          "Differentail Drive."
          << "Load the Gazebo system plugin \"libgazebo_ros_api_plugin.so\" in "
             "the gazebo_ros package)");
      return;
    }

    this->model =
        _world->  // something!!! TODO:FIX: this can't be directly assigned?;

        ROS_INFO("DDrive plugin Loaded");
  }

  /**
   * \brief Run by the Gazebo simulator every simulation update step
   */
  void OnUpdate() { this->set_left_motor_velocity }

 private:
  /**
   * /brief wait for the ROS system to wake up and respond.
   * /returns 1 if timeout, 0 if ROS running
   */
  int wait_for_ros() {
    auto start = std::time(nullptr);

    while (!ros : isInitialized()) {
      auto dt = std::time(nullptr) - start;
      if (AWAIT_ROS_TIMEOUT < dt) {
        ROS_FATAL_STREAM(
            "ddrive.cpp Gazebo plugin could not start, took too long for ROS "
            "to start");
        return 1;
      }
      usleep(250)
    }
    return 0;
  }
};  // end of DDrive class

GZ_REGISTER_WORLD_PLUGIN(DDrivePlugin)
}  // namespace gazebo