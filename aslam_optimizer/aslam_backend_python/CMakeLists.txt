cmake_minimum_required(VERSION 3.8)
project(aslam_backend_python)

set(CMAKE_CXX_STANDARD 14)
add_definitions(-fPIC -Wextra -Winit-self -Woverloaded-virtual -Wnon-virtual-dtor -Wsign-promo -Wno-long-long)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(aslam_backend REQUIRED)
find_package(aslam_backend_expressions REQUIRED)
find_package(numpy_eigen REQUIRED)
find_package(sparse_block_matrix REQUIRED)
find_package(sm_common REQUIRED)
find_package(sm_kinematics REQUIRED)
find_package(sm_timing REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development NumPy)
find_package(Boost REQUIRED COMPONENTS thread python312)

ament_python_install_package(aslam_backend PACKAGE_DIR python/aslam_backend)

include_directories(include
  ${aslam_backend_INCLUDE_DIRS}
  ${aslam_backend_expressions_INCLUDE_DIRS}
  ${numpy_eigen_INCLUDE_DIRS}
  ${sparse_block_matrix_INCLUDE_DIRS}
  ${sm_common_INCLUDE_DIRS}
  ${sm_kinematics_INCLUDE_DIRS}
  ${sm_timing_INCLUDE_DIRS}
)

add_library(libaslam_backend_python MODULE
  src/module.cpp
  src/Backend.cpp
  src/Optimizer.cpp
  src/OptimizerOptions.cpp
  src/OptimizationProblem.cpp
  src/DesignVariable.cpp
  src/ErrorTerm.cpp
  src/MEstimators.cpp
  src/JacobianContainer.cpp
  src/BackendExpressions.cpp
  src/CompressedColumnMatrix.cpp
  src/LinearSystemSolver.cpp
  src/ErrorTermTransformation.cpp
  src/TrustRegionPolicies.cpp
  src/SparseBlockMatrix.cpp
)
set_target_properties(libaslam_backend_python PROPERTIES
  PREFIX ""
  OUTPUT_NAME "libaslam_backend_python"
  SUFFIX ".so"
)
target_include_directories(libaslam_backend_python PRIVATE
  ${Python3_INCLUDE_DIRS}
  ${Python3_NumPy_INCLUDE_DIRS}
)
target_link_libraries(libaslam_backend_python PRIVATE
  Boost::python312
  ${Boost_LIBRARIES}
  Python3::Python
  ${aslam_backend_LIBRARIES}
  ${aslam_backend_expressions_LIBRARIES}
  ${sparse_block_matrix_LIBRARIES}
  ${sm_common_LIBRARIES}
  ${sm_kinematics_LIBRARIES}
  ${sm_timing_LIBRARIES}
)

install(TARGETS libaslam_backend_python
  DESTINATION ${PYTHON_INSTALL_DIR}/aslam_backend
)

install(DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include)
ament_export_dependencies(aslam_backend aslam_backend_expressions numpy_eigen sparse_block_matrix sm_common sm_kinematics sm_timing)

ament_package()
