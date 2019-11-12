docker run -it -v "/usr/local/google/home/veblush/git/abseil-cpp:/abseil" rsmmr/clang /bin/bash

$ export CC=/opt/clang/bin/clang
$ export CXX=/opt/clang/bin/clang++

$ mkdir -p abseil/test/build
$ cd abseil/test/build
$ cmake ..
