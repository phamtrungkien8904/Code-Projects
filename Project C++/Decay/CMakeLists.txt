cmake_minimum_required(VERSION 3.10)
project(RadioactiveDecaySimulation)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find SFML
find_package(SFML 2.5 COMPONENTS graphics window system REQUIRED)

# Add executable
add_executable(decay main.cpp)

# Link SFML libraries
target_link_libraries(decay sfml-graphics sfml-window sfml-system)

