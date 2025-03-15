cmake_minimum_required(VERSION 3.10)
project(MagneticBottleSimulation)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find SFML
find_package(SFML 2.5 COMPONENTS graphics window system REQUIRED)

# Source files
set(SOURCES
    main.cpp
    MagneticField.cpp
    Electron.cpp
    Simulation.cpp
    Renderer.cpp
)

# Headers
set(HEADERS
    Vector3.h
    MagneticField.h
    Electron.h
    Simulation.h
    Renderer.h
)

# Create executable
add_executable(magneticbottle ${SOURCES} ${HEADERS})

# Link with SFML
target_link_libraries(magneticbottle sfml-graphics sfml-window sfml-system)

