cmake_minimum_required(VERSION 3.22.1)
project(orbit)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
set(CMAKE_CXX_FLAGS "-Wall -Wextra")

# Add the executable with the correct source file
add_executable(orbit test.cpp)

# Find and link SFML packages correctly
find_package(SFML 2 REQUIRED graphics window system)
target_link_libraries(orbit sfml-graphics sfml-window sfml-system)

# Include directories
target_include_directories(orbit PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})