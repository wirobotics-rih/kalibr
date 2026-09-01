cmake_minimum_required(VERSION 3.8)
project(aslam_cameras_april)

add_definitions(-DASLAM_USE_ROS)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(sm_python REQUIRED)
find_package(aslam_cameras REQUIRED)
find_package(ethz_apriltag2 REQUIRED)
find_package(numpy_eigen REQUIRED)
find_package(sm_common REQUIRED)
find_package(sm_logging REQUIRED)
find_package(sm_boost REQUIRED)
find_package(sm_eigen REQUIRED)
find_package(OpenCV REQUIRED)
find_package(Boost REQUIRED COMPONENTS serialization system)
find_package(Eigen3 REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development NumPy)
find_package(Boost REQUIRED COMPONENTS python312)

ament_python_install_package(${PROJECT_NAME} PACKAGE_DIR python/${PROJECT_NAME})

include_directories(include
  ${sm_python_INCLUDE_DIRS}
  ${aslam_cameras_INCLUDE_DIRS}
  ${ethz_apriltag2_INCLUDE_DIRS}
  ${numpy_eigen_INCLUDE_DIRS}
  ${sm_common_INCLUDE_DIRS}
  ${sm_logging_INCLUDE_DIRS}
  ${sm_boost_INCLUDE_DIRS}
  ${sm_eigen_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIR}
)

add_library(${PROJECT_NAME} SHARED
  src/GridCalibrationTargetAprilgrid.cpp
)
target_link_libraries(${PROJECT_NAME}
  ${aslam_cameras_LIBRARIES}
  ${ethz_apriltag2_LIBRARIES}
  ${OpenCV_LIBS}
  ${Boost_LIBRARIES}
)

add_library(libaslam_cameras_april_python MODULE
  src/module.cpp
)
set_target_properties(libaslam_cameras_april_python PROPERTIES
  PREFIX ""
  OUTPUT_NAME "libaslam_cameras_april_python"
  SUFFIX ".so"
)
target_include_directories(libaslam_cameras_april_python PRIVATE
  ${Python3_INCLUDE_DIRS}
  ${Python3_NumPy_INCLUDE_DIRS}
)
target_link_libraries(libaslam_cameras_april_python PRIVATE
  Boost::python312
  ${Boost_LIBRARIES}
  Python3::Python
  ${PROJECT_NAME}
)

install(TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(TARGETS libaslam_cameras_april_python
  DESTINATION ${PYTHON_INSTALL_DIR}/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include)
ament_export_libraries(${PROJECT_NAME})
ament_export_dependencies(sm_python aslam_cameras ethz_apriltag2 numpy_eigen sm_common sm_logging sm_boost sm_eigen OpenCV Boost)

ament_package()
