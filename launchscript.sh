#!/bin/bash
source /opt/ros/melodic/setup.bash
source install/setup.bash
roslaunch autoware_launch autoware.launch map_path:=${HOME}/AutowareArchitectureProposal/ rosbag:=true ndt_threads:=8 ndt_debug_tool:="valgrind --tool=massif" ndt_neighborsearch_method:=3




# example of ndt_debug_tool
# In my laptop, I had to set ndt_threads:=8 for reasonal profiling.
## perf
# perf record -g -e cache-misses -o ndt.***.dat
### perf events
### system
### cycles,instructions,cache-references,cache-misses,bus-cycles,page-faults
### L1
### L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores
### LL
### LLC-loads,LLC-load-misses,LLC-stores,LLC-prefetches
## valgrind
# valgrind --tool=massif
## pin (intel tool)
# pin -t inscount*.so --
