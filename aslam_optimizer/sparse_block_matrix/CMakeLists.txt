cmake_minimum_required(VERSION 3.8)
project(sparse_block_matrix)

find_package(ament_cmake REQUIRED)
find_package(sm_common REQUIRED)
find_package(sm_eigen REQUIRED)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/cmake)

# Workaround for build machines where `libsuitesparse-dev` cannot be
# installed via apt (no sudo access): if a SuiteSparse tree was manually
# unpacked (e.g. `dpkg-deb -x` of the .deb files) into this local prefix,
# point FindSuiteSparse.cmake at it. Harmless no-op once the real
# `libsuitesparse-dev` system package is installed.
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

find_package(SuiteSparse REQUIRED)
find_package(TBB REQUIRED)
find_package(Eigen3 REQUIRED)

include_directories(
  include
  ${sm_common_INCLUDE_DIRS}
  ${sm_eigen_INCLUDE_DIRS}
  ${SUITESPARSE_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME} SHARED
  src/matrix_structure.cpp
  src/sparse_helper.cpp
  src/marginal_covariance_cholesky.cpp
)
target_link_libraries(${PROJECT_NAME}
  ${sm_common_LIBRARIES}
  ${sm_eigen_LIBRARIES}
  ${SUITESPARSE_LIBRARIES}
  TBB::tbb
)

install(TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)
install(DIRECTORY include/
  DESTINATION include
)
install(FILES cmake/FindSuiteSparse.cmake DESTINATION share/${PROJECT_NAME}/cmake/)

# Also export SuiteSparse's include dirs: downstream packages transitively
# include sparse_block_matrix headers that #include <cholmod.h> etc, even
# though they don't need to link SuiteSparse's libraries directly (only
# sparse_block_matrix.so and aslam_backend.so call into cholmod/spqr; they
# already carry the needed RPATH).
ament_export_include_directories(include ${SUITESPARSE_INCLUDE_DIRS})
ament_export_libraries(${PROJECT_NAME})
ament_export_dependencies(sm_common sm_eigen)

ament_package()
