cmake_minimum_required(VERSION 3.8)
project(sm_common)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -D__STRICT_ANSI__")

find_package(ament_cmake REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)

include_directories(include ${Boost_INCLUDE_DIRS})

add_library(${PROJECT_NAME} SHARED
  src/progress_info.cpp
)
target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})
target_compile_options(${PROJECT_NAME} PUBLIC "-Wno-deprecated-copy")

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
ament_export_dependencies(Boost)

ament_package()
