cmake_minimum_required(VERSION 3.0)
project(AP_eqvio VERSION 0.1)
set(CMAKE_CXX_STANDARD 17)

# Set off if you want to build the project in pure cmake


# include(CMakeDependentOption)
find_package(OpenCV REQUIRED)

# include_directories(
#   include
# )


## Declare a C++ library
# add_library(uartlib
#   include/serial_port.h
#   src/serial_port.cpp
# )


add_executable(camtest main.cpp)
# target_link_libraries(uart_test
# uartlib
# )

target_link_libraries(camtest
    ${OpenCV_LIBS}
)

target_include_directories(camtest
    PRIVATE ${OpenCV_INCLUDE_DIRS}
)
# Add the tests
