cmake_minimum_required(VERSION 3.8)
project(incremental_calibration_python)

set(CMAKE_CXX_STANDARD 14)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(aslam_backend REQUIRED)
find_package(incremental_calibration REQUIRED)
find_package(numpy_eigen REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development NumPy)
find_package(Boost REQUIRED COMPONENTS python312)

ament_python_install_package(incremental_calibration PACKAGE_DIR src/incremental_calibration)

include_directories(include
  ${aslam_backend_INCLUDE_DIRS}
  ${incremental_calibration_INCLUDE_DIRS}
  ${numpy_eigen_INCLUDE_DIRS}
)

add_library(libincremental_calibration_python MODULE
  src/module.cpp
  src/OptimizationProblem.cpp
  src/IncrementalEstimator.cpp
  src/LinearSolver.cpp
)
set_target_properties(libincremental_calibration_python PROPERTIES
  PREFIX ""
  OUTPUT_NAME "libincremental_calibration_python"
  SUFFIX ".so"
)
target_include_directories(libincremental_calibration_python PRIVATE
  ${Python3_INCLUDE_DIRS}
  ${Python3_NumPy_INCLUDE_DIRS}
)
target_link_libraries(libincremental_calibration_python PRIVATE
  Boost::python312
  ${Boost_LIBRARIES}
  Python3::Python
  ${aslam_backend_LIBRARIES}
  ${incremental_calibration_LIBRARIES}
)

install(TARGETS libincremental_calibration_python
  DESTINATION ${PYTHON_INSTALL_DIR}/incremental_calibration
)

install(DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include)
ament_export_dependencies(aslam_backend incremental_calibration numpy_eigen)

ament_package()
