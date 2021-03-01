#!/bin/sh
. /opt/ros/melodic/setup.sh

if [ $# -eq 0 ]; then
#    PACKAGES="ndt_scan_matcher ndt_omp"
    PACKAGES="autoware_launch sensing_launch vehicle_launch hachinoji_description"
    BUILD_TYPE=Release
    echo "build ${PACKAGES}"
    colcon build --catkin-skip-building-tests --cmake-clean-cache --cmake-args "-DCMAKE_BUILD_TYPE=${BUILD_TYPE}" --packages-select ${PACKAGES}
elif [ $1 = "all" ]; then
    colcon build --catkin-skip-building-tests --cmake-clean-cache --cmake-clean-first --cmake-args "-DCMAKE_BUILD_TYPE=Release"
fi
