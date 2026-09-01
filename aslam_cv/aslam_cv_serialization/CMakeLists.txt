cmake_minimum_required(VERSION 3.8)
project(aslam_cv_serialization)

find_package(ament_cmake REQUIRED)
find_package(aslam_cameras REQUIRED)
find_package(aslam_time REQUIRED)
find_package(sm_common REQUIRED)
find_package(sm_boost REQUIRED)
find_package(sm_property_tree REQUIRED)
find_package(sm_eigen REQUIRED)
find_package(sm_kinematics REQUIRED)
find_package(sm_opencv REQUIRED)
find_package(sm_logging REQUIRED)
find_package(sm_random REQUIRED)
find_package(Boost REQUIRED COMPONENTS serialization system)
find_package(Eigen3 REQUIRED)

include(autogen_cameras.cmake)

include_directories(include
  ${aslam_cameras_INCLUDE_DIRS}
  ${aslam_time_INCLUDE_DIRS}
  ${sm_common_INCLUDE_DIRS}
  ${sm_boost_INCLUDE_DIRS}
  ${sm_property_tree_INCLUDE_DIRS}
  ${sm_eigen_INCLUDE_DIRS}
  ${sm_kinematics_INCLUDE_DIRS}
  ${sm_opencv_INCLUDE_DIRS}
  ${sm_logging_INCLUDE_DIRS}
  ${sm_random_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME} SHARED
  ${AUTOGEN_CAMERA_CPP_FILES}
  src/FrameBaseSerialization.cpp
)
target_link_libraries(${PROJECT_NAME}
  ${aslam_cameras_LIBRARIES}
  ${aslam_time_LIBRARIES}
  ${sm_common_LIBRARIES}
  ${sm_boost_LIBRARIES}
  ${sm_property_tree_LIBRARIES}
  ${sm_eigen_LIBRARIES}
  ${sm_kinematics_LIBRARIES}
  ${sm_logging_LIBRARIES}
  ${sm_random_LIBRARIES}
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
ament_export_dependencies(aslam_cameras aslam_time sm_common sm_boost sm_property_tree sm_eigen sm_kinematics sm_opencv sm_logging sm_random Boost)

ament_package()
