# Nvidia2 Install

This is the notes for the Nvidia2 GPU acceleration install

- __NOTE:__ Nvidia docs say that this is deprecated, but the OSRF docker
  images do not seem to work with anything else!


## NVIDIA setup

- apt-get purge nvidia-docker

## Overview

- [ ] Install Docker

- [ ] Install NVIDIA Drivers:
    1. Do Pre-Install Checks
    2. Do Package Manager Install
    4. Download the NVIDIA toolkit

- [ ] Install The NVIDIA Docker packages

- [ ] Do Post Install Checks

- [ ] Install the NVIDIA Docker2 packages: `sudo apt-get install nvidia-docker2`

- [ ] Restart the Docker Daemon to use these: `sudo pkill -SIGHUP dockerd` 

------------------------------------------------------------------------------------------------------------------------
## NVIDIA Driver

- `nvidia-docker2` is the set of packages that makes NVIDIA work with Docker
- You must install the NVIDIA drivers on the host system _first_, this is why this is so complex. There are 
  two different components.


### Pre Install
[This is](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#pre-installation-actions) 
a sequences of checks that need to be performed to ensure that 
the hardware and OS of the host machine is setup correctly.

- `lspci | grep -i nvidia`
    - is NVIDIA hardware present?
- ` uname -m && cat /etc/*release`
    - is this a supported Linux OS and Chipset?
- `gcc --version`
    - is the gcc available
- `uname -r`
    - check kernel version

- `sudo apt-get install linux-headers-$(uname -r)` Install the Kernel Headers


### NVIDIA Toolkit Download
- [see](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1804&target_type=debnetwork) for instructions:

- `wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin`
- `sudo mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600`
- `sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub`
- `sudo add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /"`
- `sudo apt-get update`
- `sudo apt-get -y install cuda`

### Post Installation
https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#post-installation-actions

#### Env Setup
- `export PATH=/usr/local/cuda-10.1/bin:/usr/local/cuda-10.1/NsightCompute-2019.1${PATH:+:${PATH}}`

#### Power9 Setup
- check status of driver with `systemctl status nvidia-persistenced`
    - if not active, `sudo systemctl enable nvidia-persistenced`
- __TODO:__ is Udev rule necessary??

### Install Verification
- driver check: `cat /proc/driver/nvidia/version`

### Optinal Extras
- `sudo apt-get install g++ freeglut3-dev build-essential libx11-dev \
    libxmu-dev libxi-dev libglu1-mesa libglu1-mesa-dev`
- Just how "optional" these are in the current context is unclear

## NVIDIA Docker Packages Install
1. `curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -`
2. `distribution=$(. /etc/os-release;echo $ID$VERSION_ID)`
3. `curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.dnvidia-docker.list`
4. `sudo apt-get update`
5. `sudo apt-get install nvidia-docker2`







## Sources

- [1](https://github.com/NVIDIA/nvidia-docker/wiki/Installation-(version-2.0))
- [2](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#ubuntu-installation)