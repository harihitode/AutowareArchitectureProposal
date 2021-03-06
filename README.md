# Let's Do Profiling on NDT Scan Matcher

Profiling repository of "ndt_scan_matcher", one of the heaviest node on [Autoware architecture proposal](https://github.com/tier4/AutowareArchitectureProposal).

> **WARNING**: This source is solely for demonstrating an architecture proposal. It should not be used to drive cars.

Architecture overview is [here](/design/Overview.md).

# How to setup

## Requirements

### Hardware
- x86 CPU (8 or more cores)
- 16 GB or more of memory
- Nvidia GPU (4GB or more of memory) :

### Software
- Ubuntu 18.04
- Nvidia driver

If cuda or tensorRT is already installed, it is recommended to remove it.

## Autoware setup
1. Clone this repository
```
git clone https://github.com/tier4/AutowareArchitectureProposal.git
cd AutowareArchitectureProposal/
```
2. Run the setup script
```
./setup_ubuntu18.04.sh
```
In this step, the following software are installed.
Please confirm their licenses before using them.

- [osqp](https://github.com/oxfordcontrol/osqp/blob/master/LICENSE)
- [ROS Melodic](https://github.com/ros/ros/blob/noetic-devel/LICENSE)
- [CUDA 10.2](https://docs.nvidia.com/cuda/eula/index.html)
- [cuDNN 7](https://docs.nvidia.com/deeplearning/sdk/cudnn-sla/index.html)
- [TensorRT 7](https://docs.nvidia.com/deeplearning/sdk/tensorrt-sla/index.html)
- [geographiclib-tools](https://geographiclib.sourceforge.io/html/LICENSE.txt)

3. Build the source
```
colcon build --cmake-args "-DCMAKE_BUILD_TYPE=Debug" --catkin-skip-building-tests
```
Notes

1. Your computer need to be connected to Internet to download neural network weight files.
2. The ndt_omp does not run work -O0, -O1 optimization level. See its CMakeLists.txt for compile flag.

see buildscript.sh for daily use.

# How to run

## Simulator
![sim](https://user-images.githubusercontent.com/8327598/79709776-0bd47b00-82fe-11ea-872e-d94ef25bc3bf.png)


### Quick Start
#### Rosbag
1. Download sample map from [here](https://drive.google.com/open?id=1ovrJcFS5CZ2H51D8xVWNtEvj_oiXW-zk) and extract the zip file.

2. Download sample rosbag from [here](https://drive.google.com/open?id=1BFcNjIBUVKwupPByATYczv2X4qZtdAeD).
3. Launch Autoware
```
source install/setup.bash
roslaunch autoware_launch autoware.launch map_path:=[path] rosbag:=true ndt_threads:=[N]
```
or as blow to use debug tool for ndt_scan_matcher
```
source install/setup.bash
roslaunch autoware_launch autoware.launch map_path:=[path] rosbag:=true ndt_threads:=[N] ndt_debug_tool="perf record -g -e cache-misses -o ndt.cache-miss"
```

see launchscript.sh

4. Play rosbag
```
rosbag play --clock [rosbag file] -r 0.2
```

##### Note
- sample map : © 2020 TierIV inc.
- rosbag : © 2020 TierIV inc.
- Image data are removed due to privacy concerns.
- Cannot run traffic light recognition
- Decreased accuracy of object detection

#### Planning Simulator
1. Download sample map from [here](https://drive.google.com/open?id=197kgRfSomZzaSbRrjWTx614le2qN-oxx) and extract the zip file.

2. Launch Autoware
```
source devel/setup.bash
roslaunch autoware_launch planning_simulator.launch map_path:=[path]
```
3. Set initial pose
4. Set goal pose
5. Push engage button.
[autoware_web_controller](http://localhost:8085/autoware_web_controller/index.html)

##### Note
- sample map : © 2020 TierIV inc.

### Tutorial in detail
See [here](https://github.com/tier4/AutowareArchitectureProposal/blob/master/docs/SimulationTutorial.md). for more information.

# References
## Videos
- [Scenario demo](https://youtu.be/kn2bIU_g0oY)
- [Obstacle avoidance in the same lane](https://youtu.be/s_4fBDixFJc)
- [Obstacle avoidance by lane change](https://youtu.be/SCIceXW9sqM)
- [Object recognition](https://youtu.be/uhhMIxe1zxQ)
- [Auto parking](https://youtu.be/e9R0F0ZJbWE)
- [360° FOV perception(Camera Lidar Fuison)](https://youtu.be/whzx-2RkVBA)
- [Robustness of localization](https://youtu.be/ydPxWB2jVnM)

## Credits
- [Neural Network Weight Files](https://github.com/tier4/AutowareArchitectureProposal/blob/master/docs/Credits.md)
