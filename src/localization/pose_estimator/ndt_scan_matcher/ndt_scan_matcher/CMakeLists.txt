cmake_minimum_required(VERSION 2.8.3)
project(ndt_scan_matcher)

add_compile_options(-std=c++14)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  tf2
  tf2_ros
  tf2_sensor_msgs
  tf2_geometry_msgs
  std_msgs
  geometry_msgs
  sensor_msgs
  nav_msgs
  visualization_msgs
  diagnostic_msgs
  # pcl_conversions # for my pcl
  # pcl_ros # for my pcl
  dynamic_reconfigure
  ndt_pcl_modified
  ndt_omp
  ndt
  autoware_localization_srvs
  eigen_conversions
)

find_package(PCL 1.8.1 EXACT REQUIRED NO_DEFAULT_PATH PATHS $ENV{DEBUG_PCL_PATH})

catkin_package(
  INCLUDE_DIRS include
)

include_directories(include ${catkin_INCLUDE_DIRS} ${PCL_INCLUDE_DIRS})

message(STATUS "catkin_lib:${catkin_LIBRARIES}")
message(STATUS "pcl_lib:${PCL_LIBRARIES}")

add_executable(ndt_scan_matcher
  src/ndt_scan_matcher_node.cpp
  src/ndt_scan_matcher_core.cpp
)

add_dependencies(ndt_scan_matcher
  ${${PROJECT_NAME}_EXPORTED_TARGETS}
  ${catkin_EXPORTED_TARGETS}
)

target_link_libraries(ndt_scan_matcher
  ${catkin_LIBRARIES}
  ${PCL_LIBRARIES}
)

install(
  TARGETS
    ndt_scan_matcher
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(
  DIRECTORY
    launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
