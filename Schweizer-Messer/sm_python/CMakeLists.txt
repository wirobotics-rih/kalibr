cmake_minimum_required(VERSION 3.8)
project(sm_python)

set(CMAKE_CXX_STANDARD 14)
add_definitions(-D__STRICT_ANSI__)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(sm_common REQUIRED)
find_package(numpy_eigen REQUIRED)
find_package(sm_kinematics REQUIRED)
find_package(sm_timing REQUIRED)
find_package(sm_logging REQUIRED)
find_package(sm_matrix_archive REQUIRED)
find_package(sm_property_tree REQUIRED)
find_package(sm_eigen REQUIRED)
find_package(sm_boost REQUIRED)
find_package(sm_random REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development NumPy)
find_package(Boost REQUIRED COMPONENTS system serialization python312)

ament_python_install_package(sm PACKAGE_DIR python/sm)

include_directories(include
  ${EIGEN3_INCLUDE_DIRS}
  ${sm_common_INCLUDE_DIRS}
  ${numpy_eigen_INCLUDE_DIRS}
  ${sm_kinematics_INCLUDE_DIRS}
  ${sm_timing_INCLUDE_DIRS}
  ${sm_logging_INCLUDE_DIRS}
  ${sm_matrix_archive_INCLUDE_DIRS}
  ${sm_property_tree_INCLUDE_DIRS}
  ${sm_eigen_INCLUDE_DIRS}
  ${sm_boost_INCLUDE_DIRS}
  ${sm_random_INCLUDE_DIRS}
)

add_library(libsm_python MODULE
  src/module.cpp
  src/export_rotational_kinematics.cpp
  src/export_rotations.cpp
  src/export_transformations.cpp
  src/export_quaternion_algebra.cpp
  src/export_homogeneous.cpp
  src/exportTransformation.cpp
  src/exportHomogeneousPoint.cpp
  src/exportTimestampCorrector.cpp
  src/exportPropertyTree.cpp
  src/exportEigen.cpp
  src/exportUncertainVector.cpp
  src/exportMatrixArchive.cpp
  src/export_kinematics_property_tree.cpp
  src/export_eigen_property_tree.cpp
  src/Logging.cpp
  src/exportNsecTime.cpp
  src/random.cpp
)
set_target_properties(libsm_python PROPERTIES
  PREFIX ""
  OUTPUT_NAME "libsm_python"
  SUFFIX ".so"
)
target_include_directories(libsm_python PRIVATE
  ${Python3_INCLUDE_DIRS}
  ${Python3_NumPy_INCLUDE_DIRS}
)
target_link_libraries(libsm_python PRIVATE
  Boost::python312
  ${Boost_LIBRARIES}
  Python3::Python
  ${sm_common_LIBRARIES}
  ${sm_kinematics_LIBRARIES}
  ${sm_timing_LIBRARIES}
  ${sm_logging_LIBRARIES}
  ${sm_matrix_archive_LIBRARIES}
  ${sm_property_tree_LIBRARIES}
  ${sm_eigen_LIBRARIES}
  ${sm_boost_LIBRARIES}
  ${sm_random_LIBRARIES}
)

install(TARGETS libsm_python
  DESTINATION ${PYTHON_INSTALL_DIR}/sm
)

install(DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include)
ament_export_dependencies(sm_common numpy_eigen sm_kinematics sm_timing sm_logging sm_matrix_archive sm_property_tree sm_eigen sm_boost sm_random Boost Eigen3)

ament_package()
