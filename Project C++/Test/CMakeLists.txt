cmake_minimum_required(VERSION 3.22.1)
project(Test)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
set(CMAKE_CXX_FLAGS "-Wall -Wextra -Werror")

add_executable(Test helloworld.cpp math.cpp)
target_include_directories(Test PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})