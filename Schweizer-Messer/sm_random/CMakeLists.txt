cmake_minimum_required(VERSION 3.8)
project(sm_random)

find_package(ament_cmake REQUIRED)

include_directories(include)

add_library(${PROJECT_NAME} SHARED
  src/random.cpp
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

ament_package()
