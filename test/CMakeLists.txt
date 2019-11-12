cmake_minimum_required(VERSION 3.5)
project(my_project)

# Pick the C++ standard to compile with.
# Abseil currently supports C++11, C++14, and C++17.
set(CMAKE_CXX_STANDARD 11)

add_subdirectory(.. ${CMAKE_CURRENT_BINARY_DIR}/abseil)

add_executable(my_exe test.cpp)

target_link_libraries(my_exe absl::algorithm)
target_link_libraries(my_exe absl::base)
target_link_libraries(my_exe absl::debugging)
target_link_libraries(my_exe absl::flags)
target_link_libraries(my_exe absl::flat_hash_map)
target_link_libraries(my_exe absl::memory)
target_link_libraries(my_exe absl::meta)
target_link_libraries(my_exe absl::numeric)
target_link_libraries(my_exe absl::strings)
target_link_libraries(my_exe absl::synchronization)
target_link_libraries(my_exe absl::time)
target_link_libraries(my_exe absl::utility)

target_compile_options(my_exe PRIVATE -std=c++11)
target_compile_options(my_exe PRIVATE -Werror)
target_compile_options(my_exe PRIVATE -Wrange-loop-analysis)
target_compile_options(my_exe PRIVATE -Wcomma)
target_compile_options(my_exe PRIVATE -Wshorten-64-to-32)
target_compile_options(my_exe PRIVATE -Wunreachable-code)
