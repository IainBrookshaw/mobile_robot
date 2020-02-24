/**
 * Mobile Robot: Basic Gazebo Plugin (revision and reference)
 * Iain Brookshaw
 * Copyright (c), 2019. All Rights Reserved
 * MIT License
 *
 * see: http://gazebosim.org/tutorials?tut=plugins_hello_world&cat=write_plugin
 */

#include <gazebo/gazebo.hh>

namespace gazebo {

/**
 * \brief simple plugin for the Gazebo Robot Simulator
 */
class WorldPluginTutorial : public WorldPlugin {
 public:
  WorldPluginTutorial() : WorldPlugin() { printf("Hello World!\n"); }

 public:
  void Load(physics::WorldPtr _world, sdf::ElementPtr _sdf) {
    // TODO: This is the main setup method for the plugin, it does nothing at
    //       this time
  }
};

GZ_REGISTER_WORLD_PLUGIN(WorldPluginTutorial)
}  // namespace gazebo