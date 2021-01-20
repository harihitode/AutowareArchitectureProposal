#!/bin/sh
. /opt/ros/melodic/setup.sh
. install/setup.sh

MAP_PATH=${HOME}/sample_map
PCD_FILE=pointcloud_map.pcd
NDT_THREADS=4
# ndt_neighborsearch_method 0:KDTREE, 1:DIRECT26, 2:DIRECT7, 3:DIRECT1
NDT_NSMETHOD=0
NDT_DEBUG=""
#NDT_DEBUG="xterm -e perf record -e cpu-cycles,instructions,cache-references,cache-misses,branch-instructions,branch-misses -o ndt.hardware.perf"
#NDT_DEBUG="perf stat -o ndt.stat.perf"
#NDT_DEBUG="xterm -e valgrind --tool=cachegrind"
# NDT_DEBUG="xterm -e perf stat -B -e cache-references,cache-misses,cycles,instructions,branches,faults,migrations,L1-dcache-load-misses,L1-dcache-loads,L1-dcache-stores,L1-icache-load-misses,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses,LLC-prefetches -o perf.caches.log"

AW_SENSING=true
AW_LOCALIZATION=true
AW_PERCEPTION=false
AW_PLANNING=false
AW_CONTROL=false
AW_RVIZ=true

# export ROS_IP=192.168.10.10
# export ROS_MASTER_URI=http://192.168.10.10:11311

roslaunch autoware_launch logging_simulator.launch vehicle_model:=lexus sensor_model:=aip_xx1 map_path:=${MAP_PATH} rosbag:=true ndt_threads:=${NDT_THREADS} ndt_neighborsearch_method:=${NDT_NSMETHOD} ndt_debug_tool:="${NDT_DEBUG}" sensing:=${AW_SENSING} localization:=${AW_LOCALIZATION} perception:=${AW_PERCEPTION} planning:=${AW_PLANNING} control:=${AW_CONTCOL} rviz:="${AW_RVIZ}" pointcloud_map_file:=${PCD_FILE} ndt_dump_stats:=false
# running detection
# perception_mode:="camera_lidar_fusion" camera_number:="2"

# running massif for ndt
# ndt_debug_tool:="xterm -e valgrind --tool=massif"

# running perf record for ndt
# ndt_debug_tool:="perf record -g -e cache-misses -o ndt.***.dat"

# running pin (intel tool) for ndt
# ndt_debug_tool:="pin -t inscount*.so --"
