cmake_minimum_required(VERSION 3.8)
project(aslam_imgproc)

find_package(ament_cmake REQUIRED)
find_package(sm_common REQUIRED)
find_package(sm_eigen REQUIRED)
find_package(sm_random REQUIRED)
find_package(sm_boost REQUIRED)
find_package(sm_kinematics REQUIRED)
find_package(sm_opencv REQUIRED)
find_package(sm_logging REQUIRED)
find_package(sm_property_tree REQUIRED)
find_package(aslam_time REQUIRED)
find_package(aslam_cameras REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)
find_package(OpenCV REQUIRED)

include_directories(include
  ${sm_common_INCLUDE_DIRS}
  ${sm_eigen_INCLUDE_DIRS}
  ${sm_random_INCLUDE_DIRS}
  ${sm_boost_INCLUDE_DIRS}
  ${sm_kinematics_INCLUDE_DIRS}
  ${sm_opencv_INCLUDE_DIRS}
  ${sm_logging_INCLUDE_DIRS}
  ${sm_property_tree_INCLUDE_DIRS}
  ${aslam_time_INCLUDE_DIRS}
  ${aslam_cameras_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME} SHARED src/UndistorterBase.cpp)
target_compile_options(${PROJECT_NAME} PUBLIC -Wno-deprecated-copy -Wno-maybe-uninitialized)
target_link_libraries(${PROJECT_NAME}
  ${aslam_cameras_LIBRARIES}
  ${Boost_LIBRARIES}
  ${OpenCV_LIBS}
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
ament_export_dependencies(sm_common sm_eigen sm_random sm_boost sm_kinematics sm_opencv sm_logging sm_property_tree aslam_time aslam_cameras Boost OpenCV)

ament_package()
