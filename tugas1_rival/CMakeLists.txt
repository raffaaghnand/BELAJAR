cmake_minimum_required(VERSION 3.0)

project( run )

find_package( OpenCV REQUIRED )

add_executable( run 
    src/main.cpp 
    src/permen.cpp
    src/jaring.cpp
    src/game.cpp
)

target_link_libraries( run ${OpenCV_LIBS} )
