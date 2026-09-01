cmake_minimum_required(VERSION 3.8)
project(aslam_backend_expressions)

set(CMAKE_CXX_STANDARD 14)

find_package(ament_cmake REQUIRED)
find_package(aslam_backend REQUIRED)
find_package(sm_boost REQUIRED)
find_package(sm_random REQUIRED)
find_package(sm_kinematics REQUIRED)
find_package(sparse_block_matrix REQUIRED)
find_package(sm_timing REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)

include_directories(include
  ${aslam_backend_INCLUDE_DIRS}
  ${sm_boost_INCLUDE_DIRS}
  ${sm_random_INCLUDE_DIRS}
  ${sm_kinematics_INCLUDE_DIRS}
  ${sparse_block_matrix_INCLUDE_DIRS}
  ${sm_timing_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME} SHARED
  src/RotationExpression.cpp
  src/RotationExpressionNode.cpp
  src/RotationQuaternion.cpp
  src/MappedRotationQuaternion.cpp
  src/Vector2RotationQuaternionExpressionAdapter.cpp

  src/MatrixExpression.cpp
  src/MatrixExpressionNode.cpp
  src/MatrixTransformation.cpp

  src/TransformationExpression.cpp

  src/TransformationExpressionNode.cpp
  src/TransformationBasic.cpp

  src/EuclideanExpression.cpp
  src/EuclideanExpressionNode.cpp
  src/EuclideanPoint.cpp
  src/MappedEuclideanPoint.cpp

  src/HomogeneousExpression.cpp
  src/HomogeneousExpressionNode.cpp
  src/HomogeneousPoint.cpp
  src/MappedHomogeneousPoint.cpp

  src/ScalarExpression.cpp
  src/ScalarExpressionNode.cpp
  src/Scalar.cpp

  src/EuclideanDirection.cpp

  src/ErrorTermTransformation.cpp
  src/ErrorTermEuclidean.cpp

  src/MapTransformation.cpp

  src/MatrixBasic.cpp
)
target_link_libraries(${PROJECT_NAME}
  ${aslam_backend_LIBRARIES}
  ${sm_boost_LIBRARIES}
  ${sm_random_LIBRARIES}
  ${sm_kinematics_LIBRARIES}
  ${sparse_block_matrix_LIBRARIES}
  ${sm_timing_LIBRARIES}
  ${Boost_LIBRARIES}
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
ament_export_dependencies(aslam_backend sm_boost sm_random sm_kinematics sparse_block_matrix sm_timing Boost)

ament_package()
