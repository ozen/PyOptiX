cmake_minimum_required(VERSION 2.8.4)
project(optix_wrapper_cpp)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(SOURCE_FILES optix_python_main)

file(GLOB_RECURSE all_source "*.cpp")
file(GLOB_RECURSE all_header "*.h")
file(GLOB_RECURSE all_hpp "*.hpp")
file(REMOVE_RECURSE "build/*.*")

include_directories("objects")
include_directories("common")
include_directories("exports")
include_directories("/usr/include/python3.2")
include_directories("/usr/include/boost")
include_directories("/usr/local/optix/include/")
include_directories("/usr/local/cuda/include")

link_directories("/usr/local/lib")
link_directories("/usr/local/optix/lib64")
link_directories("/usr/local/cuda/lib64")

ADD_LIBRARY(optix_wrapper_cpp SHARED ${all_source} ${all_header} ${all_hpp} main.cpp)

TARGET_LINK_LIBRARIES(optix_wrapper_cpp optix)
TARGET_LINK_LIBRARIES(optix_wrapper_cpp optixu)
TARGET_LINK_LIBRARIES(optix_wrapper_cpp cudart)

TARGET_LINK_LIBRARIES(optix_wrapper_cpp python3.2mu)
TARGET_LINK_LIBRARIES(optix_wrapper_cpp boost_python-py32)
TARGET_LINK_LIBRARIES(optix_wrapper_cpp boost_numpy)
set_target_properties(optix_wrapper_cpp PROPERTIES PREFIX "")
