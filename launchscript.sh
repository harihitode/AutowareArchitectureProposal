#!/bin/bash
source /opt/ros/melodic/setup.bash
source install/setup.bash
roslaunch autoware_launch autoware.launch map_path:=${HOME}/AutowareArchitectureProposal/ rosbag:=true ndt_threads:=8 ndt_debug_tool:="" ndt_neighborsearch_method:=3
