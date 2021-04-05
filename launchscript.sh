#!/bin/sh
. install/setup.sh

MAP_PATH=${HOME}/sample
PCD_FILE=pointcloud_map.pcd
NDT_THREADS=4
# ndt_neighborsearch_method 0:KDTREE, 1:DIRECT26, 2:DIRECT7, 3:DIRECT1
NDT_NSMETHOD=0
NDT_DEBUG=""

AW_SENSING=true
AW_LOCALIZATION=true
AW_PERCEPTION=false
AW_PLANNING=false
AW_CONTROL=false
AW_RVIZ=true

# export ROS_IP=192.168.10.10
# export ROS_MASTER_URI=http://192.168.10.10:11311

ros2 launch autoware_launch logging_simulator.launch.xml vehicle_model:=lexus sensor_model:=aip_xx1 map_path:=${MAP_PATH} perception:=${AW_PERCEPTION} planning:=${AW_PLANNING} control:=${AW_CONTROL} rviz:="${AW_RVIZ}" pointcloud_map_file:=${PCD_FILE}
# running detection
# perception_mode:="camera_lidar_fusion" camera_number:="2"

# running massif for ndt
# ndt_debug_tool:="xterm -e valgrind --tool=massif"

# running perf record for ndt
# ndt_debug_tool:="perf record -g -e cache-misses -o ndt.***.dat"

# running pin (intel tool) for ndt
# ndt_debug_tool:="pin -t inscount*.so --"
