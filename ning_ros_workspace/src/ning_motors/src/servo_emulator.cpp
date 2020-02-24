/**
 * Ningauble of The Seven Eyes
 * Iain Brookshaw
 * Copyright (c), 2020. All Rights Reserved
 * MIT License
 */
#include "ning_motors/servo_emulator.hpp"

using namespace gazebo;

ServoPidController::ServoPidController() {
    ServoPidController(ServoPidController::default_p, ServoPidController::default_i, ServoPidController::default_d);
}
ServoPidController::ServoPidController(double p, double i, double d) {
    this->p = p;
    this->i = i;
    this->d = d;
}

ServoParams::ServoParams() {
    this->max_rotation_rads = ServoParams::defaultMaxRotationRads;
    this->min_rotation_rads = ServoParams::defaultMinRotationRads;
    this->max_velocity_rads_per_sec = ServoParams::defaultMaxRotationRadsPerSec;
    this->max_torque_nm = ServoParams::defaultTorqueRadsPerSec;
}

// ---------------------------------------------------------------------------------------------------------------------
// Servo Motor
//

ServoMotor::ServoMotor(physics::ModelPtr drive_model, ServoParams params, ServoPidController pid) {
    if (!drive_model) throw std::runtime_error("Servo Motor was passed a null model pointer");
    ServoMotor::_validateParams(params);

    this->_model_ptr = drive_model;
    this->_params = params;
    this->_pid = pid;
}

ServoMotor::ServoMotor(physics::ModelPtr drive_model, ServoParams params) {
    ServoPidController pid;
    pid.timestamp = 0.0;
    pid.target = 0.0;
    pid.current = 0.0;
    this->ServoMotor(drive_model, params, pid);
}

ServoMotor::ServoMotor(physics::ModelPtr drive_model) {
    ServoParams params;
    ServoMotor(drive_model, params);
}

double ServoMotor::_computeNewPose(double new_time, ServoController& pid, ServoParams& params) { double dt = }