cmake_minimum_required(VERSION 3.8)
project(incremental_calibration)

set(CMAKE_CXX_STANDARD 14)

find_package(ament_cmake REQUIRED)
find_package(sm_eigen REQUIRED)
find_package(aslam_backend REQUIRED)
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
find_package(sparse_block_matrix REQUIRED)
find_package(SuiteSparse REQUIRED)

include_directories(include
  ${sm_eigen_INCLUDE_DIRS}
  ${aslam_backend_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIR}
  ${SUITESPARSE_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME} SHARED
  src/base/Serializable.cpp
  src/base/Timestamp.cpp
  src/base/Condition.cpp
  src/base/Mutex.cpp
  src/base/Thread.cpp
  src/base/Threads.cpp
  src/base/Timer.cpp
  src/exceptions/Exception.cpp
  src/exceptions/InvalidOperationException.cpp
  src/exceptions/NullPointerException.cpp
  src/exceptions/SystemException.cpp
  src/statistics/NormalDistribution1v.cpp
  src/statistics/ChiSquareDistribution.cpp
  src/statistics/EstimatorMLNormal1v.cpp
  src/functions/IncompleteGammaPFunction.cpp
  src/functions/IncompleteGammaQFunction.cpp
  src/functions/LogFactorialFunction.cpp
  src/functions/LogGammaFunction.cpp
  src/core/IncrementalEstimator.cpp
  src/core/OptimizationProblem.cpp
  src/core/IncrementalOptimizationProblem.cpp
  src/core/LinearSolver.cpp
  src/core/LinearSolverOptions.cpp
  src/algorithms/marginalize.cpp
  src/algorithms/linalg.cpp
)
target_link_libraries(${PROJECT_NAME}
  ${aslam_backend_LIBRARIES}
  ${sm_eigen_LIBRARIES}
  ${Boost_LIBRARIES}
  TBB::tbb
  ${SUITESPARSE_LIBRARIES}
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
ament_export_dependencies(sm_eigen aslam_backend Boost)

ament_package()
