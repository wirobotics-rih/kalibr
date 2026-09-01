cmake_minimum_required(VERSION 3.8)
project(sm_opencv)

set(CMAKE_CXX_STANDARD 14)
add_definitions(-D__STRICT_ANSI__)

find_package(ament_cmake REQUIRED)
find_package(sm_common REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)
find_package(OpenCV REQUIRED)

include_directories(include ${sm_common_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS} ${OpenCV_INCLUDE_DIRS})

install(DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include)
ament_export_dependencies(sm_common Boost OpenCV)

ament_package()
