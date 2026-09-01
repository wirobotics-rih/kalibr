cmake_minimum_required(VERSION 3.8)
project(aslam_cv_backend)

find_package(ament_cmake REQUIRED)
find_package(sm_common REQUIRED)
find_package(sm_boost REQUIRED)
find_package(sm_kinematics REQUIRED)
find_package(sm_eigen REQUIRED)
find_package(sm_opencv REQUIRED)
find_package(sm_property_tree REQUIRED)
find_package(sm_logging REQUIRED)
find_package(sm_timing REQUIRED)
find_package(aslam_backend REQUIRED)
find_package(aslam_backend_expressions REQUIRED)
find_package(aslam_time REQUIRED)
find_package(aslam_cameras REQUIRED)
find_package(sparse_block_matrix REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)

include_directories(include
  ${sm_common_INCLUDE_DIRS}
  ${sm_boost_INCLUDE_DIRS}
  ${sm_kinematics_INCLUDE_DIRS}
  ${sm_eigen_INCLUDE_DIRS}
  ${sm_opencv_INCLUDE_DIRS}
  ${sm_property_tree_INCLUDE_DIRS}
  ${sm_logging_INCLUDE_DIRS}
  ${sm_timing_INCLUDE_DIRS}
  ${aslam_backend_INCLUDE_DIRS}
  ${aslam_backend_expressions_INCLUDE_DIRS}
  ${aslam_time_INCLUDE_DIRS}
  ${aslam_cameras_INCLUDE_DIRS}
  ${sparse_block_matrix_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME} SHARED
  src/GridCalibrationTargetDesignVariableContainer.cpp
)
target_link_libraries(${PROJECT_NAME}
  ${aslam_backend_LIBRARIES}
  ${aslam_backend_expressions_LIBRARIES}
  ${aslam_time_LIBRARIES}
  ${aslam_cameras_LIBRARIES}
  ${Boost_LIBRARIES}
)

install(TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include)
ament_export_libraries(${PROJECT_NAME})
ament_export_dependencies(sm_common sm_boost sm_kinematics sm_eigen sm_opencv sm_property_tree sm_logging sm_timing aslam_backend aslam_backend_expressions aslam_time aslam_cameras sparse_block_matrix Boost)

ament_package()
