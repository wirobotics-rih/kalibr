cmake_minimum_required(VERSION 3.8)
project(aslam_backend)

set(CMAKE_CXX_STANDARD 14)

find_package(ament_cmake REQUIRED)
find_package(sparse_block_matrix REQUIRED)
find_package(sm_boost REQUIRED)
find_package(sm_random REQUIRED)
find_package(sm_timing REQUIRED)
find_package(sm_logging REQUIRED)
find_package(sm_property_tree REQUIRED)
find_package(Boost REQUIRED COMPONENTS system thread)
find_package(Eigen3 REQUIRED)
find_package(TBB REQUIRED)

# Workaround for build machines where `libsuitesparse-dev` cannot be
# installed via apt (no sudo access). See sparse_block_matrix/CMakeLists.txt.
set(SUITESPARSE_LOCAL_PREFIX "$ENV{HOME}/.local/opt/suitesparse/usr")
if(EXISTS "${SUITESPARSE_LOCAL_PREFIX}")
  list(APPEND SUITESPARSE_INCLUDE_DIR_HINTS
    "${SUITESPARSE_LOCAL_PREFIX}/include"
    "${SUITESPARSE_LOCAL_PREFIX}/include/suitesparse")
  list(APPEND SUITESPARSE_LIBRARY_DIR_HINTS
    "${SUITESPARSE_LOCAL_PREFIX}/lib/x86_64-linux-gnu")
  set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
  set(CMAKE_INSTALL_RPATH "${SUITESPARSE_LOCAL_PREFIX}/lib/x86_64-linux-gnu")
endif()
list(APPEND CMAKE_MODULE_PATH ${sparse_block_matrix_DIR})
find_package(SuiteSparse REQUIRED)

include_directories(include
  ${sparse_block_matrix_INCLUDE_DIRS}
  ${sm_boost_INCLUDE_DIRS}
  ${sm_random_INCLUDE_DIRS}
  ${sm_timing_INCLUDE_DIRS}
  ${sm_logging_INCLUDE_DIRS}
  ${sm_property_tree_INCLUDE_DIRS}
  ${Boost_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
  ${SUITESPARSE_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME} SHARED
  src/MEstimatorPolicies.cpp
  src/JacobianContainer.cpp
  src/DesignVariable.cpp
  src/ErrorTerm.cpp
  src/OptimizationProblemBase.cpp
  src/Optimizer.cpp
  src/sparse_matrix_functions.cpp
  src/OptimizationProblem.cpp
  src/SimpleOptimizationProblem.cpp
  src/JacobianBuilder.cpp
  src/LinearSystemSolver.cpp
  src/BlockCholeskyLinearSystemSolver.cpp
  src/SparseCholeskyLinearSystemSolver.cpp
  src/SparseQrLinearSystemSolver.cpp
  src/Matrix.cpp
  src/DenseMatrix.cpp
  src/SparseBlockMatrixWrapper.cpp
  src/DenseQrLinearSystemSolver.cpp
  src/BlockCholeskyLinearSolverOptions.cpp
  src/SparseCholeskyLinearSolverOptions.cpp
  src/SparseQRLinearSolverOptions.cpp
  src/DenseQRLinearSolverOptions.cpp
  src/TrustRegionPolicy.cpp
  src/ErrorTermDs.cpp
  src/GaussNewtonTrustRegionPolicy.cpp
  src/LevenbergMarquardtTrustRegionPolicy.cpp
  src/Marginalizer.cpp
  src/MarginalizationPriorErrorTerm.cpp
  src/DogLegTrustRegionPolicy.cpp
  src/Optimizer2.cpp
)
target_link_libraries(${PROJECT_NAME}
  ${Boost_LIBRARIES}
  TBB::tbb
  ${SUITESPARSE_LIBRARIES}
  ${sparse_block_matrix_LIBRARIES}
  ${sm_boost_LIBRARIES}
  ${sm_random_LIBRARIES}
  ${sm_timing_LIBRARIES}
  ${sm_logging_LIBRARIES}
  ${sm_property_tree_LIBRARIES}
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
ament_export_dependencies(sparse_block_matrix sm_boost sm_random sm_timing sm_logging sm_property_tree Boost)

ament_package()
