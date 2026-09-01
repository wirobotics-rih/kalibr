cmake_minimum_required(VERSION 3.8)
project(numpy_eigen)

set(CMAKE_CXX_STANDARD 14)
add_definitions(-D__STRICT_ANSI__)
# ignore "error: return-statement with a value, in function returning 'void'" in "__multiarray_api.h"
add_compile_options(-fpermissive)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)
find_package(Eigen3 REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development NumPy)
find_package(Boost REQUIRED COMPONENTS python312)

ament_python_install_package(${PROJECT_NAME} PACKAGE_DIR src/${PROJECT_NAME})

add_definitions(${EIGEN_DEFINITIONS})
include_directories(include ${EIGEN3_INCLUDE_DIRS})
include_directories("${PROJECT_SOURCE_DIR}/include/numpy_eigen")

include(src/autogen_files.cmake)

add_library(libnumpy_eigen MODULE ${AUTOGEN_FILES})
set_target_properties(libnumpy_eigen PROPERTIES
  PREFIX ""
  OUTPUT_NAME "libnumpy_eigen"
  SUFFIX ".so"
)
target_include_directories(libnumpy_eigen PRIVATE
  ${Python3_INCLUDE_DIRS}
  ${Python3_NumPy_INCLUDE_DIRS}
)
target_link_libraries(libnumpy_eigen PRIVATE
  Boost::python312
  ${Boost_LIBRARIES}
  Python3::Python
)

install(TARGETS libnumpy_eigen
  DESTINATION ${PYTHON_INSTALL_DIR}/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include)
ament_export_dependencies(Boost Eigen3)

ament_package()
