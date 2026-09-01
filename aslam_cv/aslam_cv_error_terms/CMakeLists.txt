cmake_minimum_required(VERSION 3.8)
project(aslam_cv_error_terms)

# Header-only package: no library is built here. NOTE: the
# CovarianceReprojectionError.hpp / BSplineMotionError.hpp headers in this
# package #include headers from aslam_splines/bsplines (camera-IMU-only
# packages that are intentionally not ported, see aslam_cv_backend_python's
# CMakeLists for the consumer-side workaround). Any *new* consumer of this
# package must avoid including those two specific headers unless
# aslam_splines/bsplines get ported too.
find_package(ament_cmake REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)

install(DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include)
ament_export_dependencies(Boost)

ament_package()
