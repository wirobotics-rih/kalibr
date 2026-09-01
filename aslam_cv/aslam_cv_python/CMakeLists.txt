cmake_minimum_required(VERSION 3.8)
project(aslam_cv_python)

set(CMAKE_CXX_STANDARD 14)
add_definitions(-fPIC -Wextra -Winit-self -Woverloaded-virtual -Wnon-virtual-dtor -Wsign-promo -Wno-long-long)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(sm_common REQUIRED)
find_package(sm_eigen REQUIRED)
find_package(sm_kinematics REQUIRED)
find_package(sm_python REQUIRED)
find_package(sm_opencv REQUIRED)
find_package(aslam_cv_serialization REQUIRED)
find_package(aslam_cameras REQUIRED)
find_package(aslam_time REQUIRED)
find_package(aslam_imgproc REQUIRED)
find_package(numpy_eigen REQUIRED)
find_package(Boost REQUIRED COMPONENTS serialization)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development NumPy)
find_package(Boost REQUIRED COMPONENTS python312)

ament_python_install_package(aslam_cv PACKAGE_DIR python/aslam_cv)

include_directories(include
  ${sm_common_INCLUDE_DIRS}
  ${sm_eigen_INCLUDE_DIRS}
  ${sm_kinematics_INCLUDE_DIRS}
  ${sm_python_INCLUDE_DIRS}
  ${sm_opencv_INCLUDE_DIRS}
  ${aslam_cv_serialization_INCLUDE_DIRS}
  ${aslam_cameras_INCLUDE_DIRS}
  ${aslam_time_INCLUDE_DIRS}
  ${aslam_imgproc_INCLUDE_DIRS}
  ${numpy_eigen_INCLUDE_DIRS}
)

add_library(libaslam_cv_python MODULE
  src/module.cpp
  src/CameraGeometries.cpp
  src/CameraGeometry.cpp
  src/Time.cpp
  src/Frontend.cpp
  src/Frame.cpp
  src/CameraProjections.cpp
  src/CameraShutters.cpp
  src/GridCalibration.cpp
  src/Undistorters.cpp
  src/OmniUndistorter.cpp
  src/PinholeUndistorter.cpp
)
set_target_properties(libaslam_cv_python PROPERTIES
  PREFIX ""
  OUTPUT_NAME "libaslam_cv_python"
  SUFFIX ".so"
)
target_compile_options(libaslam_cv_python PUBLIC "-Wno-deprecated-copy")
target_include_directories(libaslam_cv_python PRIVATE
  ${Python3_INCLUDE_DIRS}
  ${Python3_NumPy_INCLUDE_DIRS}
)
target_link_libraries(libaslam_cv_python PRIVATE
  Boost::python312
  ${Boost_LIBRARIES}
  Python3::Python
  ${aslam_cv_serialization_LIBRARIES}
  ${aslam_cameras_LIBRARIES}
  ${aslam_time_LIBRARIES}
  ${aslam_imgproc_LIBRARIES}
)

install(TARGETS libaslam_cv_python
  DESTINATION ${PYTHON_INSTALL_DIR}/aslam_cv
)

install(DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include)
ament_export_dependencies(sm_common sm_eigen sm_kinematics sm_python sm_opencv aslam_cv_serialization aslam_cameras aslam_time aslam_imgproc numpy_eigen)

ament_package()
