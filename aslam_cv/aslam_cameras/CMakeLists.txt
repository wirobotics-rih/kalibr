cmake_minimum_required(VERSION 3.8)
project(aslam_cameras)

add_definitions(-DASLAM_USE_ROS)

find_package(ament_cmake REQUIRED)
find_package(sm_common REQUIRED)
find_package(sm_eigen REQUIRED)
find_package(sm_boost REQUIRED)
find_package(sm_kinematics REQUIRED)
find_package(sm_logging REQUIRED)
find_package(aslam_time REQUIRED)
find_package(sm_opencv REQUIRED)
find_package(sm_property_tree REQUIRED)
find_package(sm_random REQUIRED)
find_package(Boost REQUIRED COMPONENTS system serialization filesystem)
find_package(Eigen3 REQUIRED)
find_package(OpenCV REQUIRED)

include_directories(include
  ${sm_common_INCLUDE_DIRS}
  ${sm_eigen_INCLUDE_DIRS}
  ${sm_boost_INCLUDE_DIRS}
  ${sm_kinematics_INCLUDE_DIRS}
  ${sm_logging_INCLUDE_DIRS}
  ${aslam_time_INCLUDE_DIRS}
  ${sm_opencv_INCLUDE_DIRS}
  ${sm_property_tree_INCLUDE_DIRS}
  ${sm_random_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIR}
  ${Boost_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME} SHARED
  src/CameraGeometryBase.cpp
  src/GlobalShutter.cpp
  src/RollingShutter.cpp
  src/NoMask.cpp
  src/NoDistortion.cpp
  src/RadialTangentialDistortion.cpp
  src/EquidistantDistortion.cpp
  src/FovDistortion.cpp
  src/ImageMask.cpp
  src/GridCalibrationTargetObservation.cpp
  src/GridCalibrationTargetBase.cpp
  src/GridCalibrationTargetCheckerboard.cpp
  src/GridCalibrationTargetCirclegrid.cpp
  src/GridDetector.cpp
  src/Triangulation.cpp
  src/FrameBase.cpp
  src/KeypointBase.cpp
  src/DescriptorBase.cpp
  src/BackProjection.cpp
  src/Landmark.cpp
  src/Image.cpp
)
target_link_libraries(${PROJECT_NAME}
  ${sm_common_LIBRARIES}
  ${sm_eigen_LIBRARIES}
  ${sm_boost_LIBRARIES}
  ${sm_kinematics_LIBRARIES}
  ${sm_logging_LIBRARIES}
  ${aslam_time_LIBRARIES}
  ${sm_property_tree_LIBRARIES}
  ${sm_random_LIBRARIES}
  ${Boost_LIBRARIES}
  ${OpenCV_LIBS}
)
target_compile_options(${PROJECT_NAME} PUBLIC "-Wno-deprecated-copy")

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
ament_export_dependencies(sm_common sm_eigen sm_boost sm_kinematics sm_logging aslam_time sm_opencv sm_property_tree sm_random Boost OpenCV)

ament_package()
