cmake_minimum_required(VERSION 3.8)
project(sm_eigen)

find_package(ament_cmake REQUIRED)
find_package(sm_common REQUIRED)
find_package(sm_random REQUIRED)
find_package(Boost REQUIRED COMPONENTS system serialization)
find_package(Eigen3 REQUIRED)

include_directories(include ${sm_common_INCLUDE_DIRS} ${sm_random_INCLUDE_DIRS} ${EIGEN3_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})

add_library(${PROJECT_NAME} SHARED
  src/random.cpp
)
target_link_libraries(${PROJECT_NAME} ${sm_common_LIBRARIES} ${sm_random_LIBRARIES} ${Boost_LIBRARIES})

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
ament_export_dependencies(sm_common sm_random Boost Eigen3)

ament_package()
