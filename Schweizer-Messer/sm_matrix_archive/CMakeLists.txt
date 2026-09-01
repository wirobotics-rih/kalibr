cmake_minimum_required(VERSION 3.8)
project(sm_matrix_archive)

set(CMAKE_CXX_STANDARD 14)
add_definitions(-D__STRICT_ANSI__)

find_package(ament_cmake REQUIRED)
find_package(sm_common REQUIRED)
find_package(Boost REQUIRED COMPONENTS system filesystem)
find_package(Eigen3 REQUIRED)

include_directories(include ${EIGEN3_INCLUDE_DIRS} ${sm_common_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})

add_library(${PROJECT_NAME} SHARED
  src/MatrixArchive.cpp
)
target_link_libraries(${PROJECT_NAME} ${sm_common_LIBRARIES} ${Boost_LIBRARIES} pthread)

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
ament_export_dependencies(sm_common Boost Eigen3)

ament_package()
