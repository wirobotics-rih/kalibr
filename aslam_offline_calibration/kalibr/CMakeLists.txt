cmake_minimum_required(VERSION 3.8)
project(kalibr)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(aslam_backend REQUIRED)
find_package(aslam_backend_expressions REQUIRED)
find_package(numpy_eigen REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development NumPy)
find_package(Boost REQUIRED COMPONENTS python312)

##################################
# error terms (+python export)
##################################
include_directories(include
  ${aslam_backend_INCLUDE_DIRS}
  ${aslam_backend_expressions_INCLUDE_DIRS}
  ${numpy_eigen_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME}_errorterms SHARED
  src/EuclideanError.cpp
  src/GyroscopeError.cpp
  src/AccelerometerError.cpp
)
target_link_libraries(${PROJECT_NAME}_errorterms
  ${aslam_backend_LIBRARIES}
  ${aslam_backend_expressions_LIBRARIES}
)

# NB: installed directly into the top level of the Python install
# directory (not nested under a kalibr_errorterms/ package dir) because
# python/kalibr_errorterms/__init__.py does a top-level
# `from libkalibr_errorterms_python import *` (a historical artifact of
# the original catkin "install to a global location" hack).
add_library(libkalibr_errorterms_python MODULE
  src/module.cpp
)
set_target_properties(libkalibr_errorterms_python PROPERTIES
  PREFIX ""
  OUTPUT_NAME "libkalibr_errorterms_python"
  SUFFIX ".so"
)
target_include_directories(libkalibr_errorterms_python PRIVATE
  ${Python3_INCLUDE_DIRS}
  ${Python3_NumPy_INCLUDE_DIRS}
)
target_link_libraries(libkalibr_errorterms_python PRIVATE
  Boost::python312
  ${Boost_LIBRARIES}
  Python3::Python
  ${PROJECT_NAME}_errorterms
)

##################################
# Python packages
##################################
ament_python_install_package(kalibr_errorterms PACKAGE_DIR python/kalibr_errorterms)
ament_python_install_package(kalibr_common PACKAGE_DIR python/kalibr_common)
ament_python_install_package(kalibr_camera_calibration PACKAGE_DIR python/kalibr_camera_calibration)
ament_python_install_package(kalibr_imu_camera_calibration PACKAGE_DIR python/kalibr_imu_camera_calibration)
ament_python_install_package(kalibr_rs_camera_calibration PACKAGE_DIR python/kalibr_rs_camera_calibration)

install(TARGETS libkalibr_errorterms_python
  DESTINATION ${PYTHON_INSTALL_DIR}
)

##################################
# executables (installed as ros2-run-able scripts)
##################################
install(PROGRAMS
    python/kalibr_bagcreater
    python/kalibr_camera_focus
    python/kalibr_bagextractor
    python/kalibr_camera_validator
    python/kalibr_visualize_calibration
    python/kalibr_calibrate_cameras
    python/kalibr_visualize_distortion
    python/kalibr_calibrate_imu_camera
    python/kalibr_create_target_pdf
    python/kalibr_calibrate_rs_cameras
  DESTINATION lib/${PROJECT_NAME}
)

install(TARGETS ${PROJECT_NAME}_errorterms
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include)
ament_export_libraries(${PROJECT_NAME}_errorterms)
ament_export_dependencies(aslam_backend aslam_backend_expressions)

ament_package()
