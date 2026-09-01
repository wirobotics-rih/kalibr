cmake_minimum_required(VERSION 3.8)
project(aslam_cv_backend_python)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(sm_common REQUIRED)
find_package(sm_python REQUIRED)
find_package(sm_opencv REQUIRED)
find_package(numpy_eigen REQUIRED)
find_package(sparse_block_matrix REQUIRED)
find_package(aslam_backend REQUIRED)
find_package(aslam_backend_expressions REQUIRED)
find_package(aslam_backend_python REQUIRED)
find_package(aslam_cameras REQUIRED)
find_package(aslam_cv_error_terms REQUIRED)
find_package(aslam_cv_backend REQUIRED)
find_package(aslam_time REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development NumPy)
find_package(Boost REQUIRED COMPONENTS python312)

ament_python_install_package(aslam_cv_backend PACKAGE_DIR python/aslam_cv_backend)

include_directories(include
  ${sm_common_INCLUDE_DIRS}
  ${sm_python_INCLUDE_DIRS}
  ${sm_opencv_INCLUDE_DIRS}
  ${numpy_eigen_INCLUDE_DIRS}
  ${sparse_block_matrix_INCLUDE_DIRS}
  ${aslam_backend_INCLUDE_DIRS}
  ${aslam_backend_expressions_INCLUDE_DIRS}
  ${aslam_backend_python_INCLUDE_DIRS}
  ${aslam_cameras_INCLUDE_DIRS}
  ${aslam_cv_error_terms_INCLUDE_DIRS}
  ${aslam_cv_backend_INCLUDE_DIRS}
  ${aslam_time_INCLUDE_DIRS}
)

add_library(libaslam_cv_backend_python MODULE
  src/module.cpp
  src/GridCalibration.cpp
)
set_target_properties(libaslam_cv_backend_python PROPERTIES
  PREFIX ""
  OUTPUT_NAME "libaslam_cv_backend_python"
  SUFFIX ".so"
)
target_include_directories(libaslam_cv_backend_python PRIVATE
  ${Python3_INCLUDE_DIRS}
  ${Python3_NumPy_INCLUDE_DIRS}
)
target_link_libraries(libaslam_cv_backend_python PRIVATE
  Boost::python312
  ${Boost_LIBRARIES}
  Python3::Python
  ${aslam_backend_LIBRARIES}
  ${aslam_backend_expressions_LIBRARIES}
  ${aslam_cameras_LIBRARIES}
  ${aslam_cv_backend_LIBRARIES}
  ${aslam_time_LIBRARIES}
)

install(TARGETS libaslam_cv_backend_python
  DESTINATION ${PYTHON_INSTALL_DIR}/aslam_cv_backend
)

install(DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include)
ament_export_dependencies(sm_common sm_python sm_opencv numpy_eigen sparse_block_matrix aslam_backend aslam_backend_expressions aslam_cameras aslam_cv_error_terms aslam_cv_backend aslam_time)

ament_package()
