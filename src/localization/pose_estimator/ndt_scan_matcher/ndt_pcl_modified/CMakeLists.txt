cmake_minimum_required(VERSION 2.8.3)
project(ndt_pcl_modified)

add_compile_options(-std=c++14)

if (DEFINED $ENV{DEBUG_PCL_PATH})
  find_package(PCL 1.8.1 EXACT REQUIRED NO_DEFAULT_PATH PATHS $ENV{DEBUG_PCL_PATH})
else()
  find_package(PCL 1.8.1 REQUIRED)
endif()

find_package(catkin REQUIRED)
catkin_package(
  INCLUDE_DIRS include
)

include_directories(include ${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

add_library(ndt_pcl_modified
  src/ndt.cpp
)

target_link_libraries(ndt_pcl_modified ${catkin_LIBRARIES})

install(
  TARGETS
    ndt_pcl_modified
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
)
