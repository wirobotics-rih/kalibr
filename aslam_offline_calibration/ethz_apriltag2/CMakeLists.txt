cmake_minimum_required(VERSION 3.8)
project(ethz_apriltag2)

add_definitions(-fPIC -O3)

find_package(ament_cmake REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(OpenCV REQUIRED)

include_directories(include ${EIGEN3_INCLUDE_DIRS})

file(GLOB SOURCE_FILES "src/*.cc")
add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})

# NOTE: the v4l2-based apriltags_demo executable (src/example/) is
# intentionally not built here: it needs libv4l-dev (headers + libv4l2),
# which is not installed and not needed for kalibr_calibrate_cameras.

install(TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include ${EIGEN3_INCLUDE_DIRS})
ament_export_libraries(${PROJECT_NAME})
ament_export_dependencies(OpenCV)

ament_package()
