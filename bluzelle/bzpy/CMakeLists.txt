cmake_minimum_required (VERSION 3.10)
project(_bzapi)

add_definitions(-D_LIBCPP_ENABLE_CXX17_REMOVED_FEATURES)

set(CMAKE_BUILD_TYPE Debug)

SET(BZAPI_PATH "../bzapi" CACHE STRING "bzapi sources path")

set(CMAKE_CXX_STANDARD 17)

include(ExternalProject)

ExternalProject_Add(bzapi_external
          SOURCE_DIR ${BZAPI_PATH}
          BINARY_DIR bzapi_bin
          CMAKE_ARGS -DSTATIC_LIBRARY=ON -DBUILD_TESTS=OFF -DBUILD_DEPEND=ON
          INSTALL_COMMAND ""
          DOWNLOAD_COMMAND "")

# use bzapi's precompiled libraries...

# boost
set(boost_lib_dir ${CMAKE_BINARY_DIR}/bzapi_bin/boost/src/boost/stage/lib)

set(Boost_LIBRARIES
    ${boost_lib_dir}/libboost_log.a
    ${boost_lib_dir}/libboost_program_options.a
    ${boost_lib_dir}/libboost_system.a
    ${boost_lib_dir}/libboost_thread.a
    pthread
    ${boost_lib_dir}/libboost_serialization.a
    ${boost_lib_dir}/libboost_date_time.a
    ${boost_lib_dir}/libboost_log_setup.a
    ${boost_lib_dir}/libboost_filesystem.a
    ${boost_lib_dir}/libboost_regex.a
    ${boost_lib_dir}/libboost_chrono.a
    ${boost_lib_dir}/libboost_atomic.a
    )

# json
set(JSONCPP_LIBRARIES ${CMAKE_BINARY_DIR}/bzapi_bin/jsoncpp/src/jsoncpp-build/src/lib_json/libjsoncpp.a)

# openssl
set(OPENSSL_LIBRARIES
    ${CMAKE_BINARY_DIR}/bzapi_bin/openssl/src/openssl-build/libssl.a
    ${CMAKE_BINARY_DIR}/bzapi_bin/openssl/src/openssl-build/libcrypto.a)

include(FindProtobuf)
find_package(Protobuf REQUIRED)
include_directories(${PROTOBUF_INCLUDE_DIR})

include(FindPkgConfig)
find_package(PythonLibs 3 REQUIRED)

if(PYTHONLIBS_VERSION_STRING MATCHES "^2.*$" )
    set(CMAKE_SWIG_FLAGS -classic -c++)
else()
    set(CMAKE_SWIG_FLAGS -py3 -c++)
endif()

find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

# generated proto files
include_directories(${CMAKE_SOURCE_DIR}/bzapi ${CMAKE_BINARY_DIR}/bzapi_bin)
include_directories(${PYTHON_INCLUDE_DIRS})

set(BZAPI_LIBRARY    ${CMAKE_BINARY_DIR}/bzapi_bin/library/libbzapi.a)
set(CRYPTO_LIBRARY   ${CMAKE_BINARY_DIR}/bzapi_bin/crypto/libcrypto.a)
set(DATABASE_LIBRARY ${CMAKE_BINARY_DIR}/bzapi_bin/database/libdatabase.a)
set(NODE_LIBRARY     ${CMAKE_BINARY_DIR}/bzapi_bin/node/libnode.a)
set(PROTO_LIBRARY    ${CMAKE_BINARY_DIR}/bzapi_bin/proto/libproto.a)
set(SWARM_LIBRARY    ${CMAKE_BINARY_DIR}/bzapi_bin/swarm/libswarm.a)
set(UTILS_LIBRARY    ${CMAKE_BINARY_DIR}/bzapi_bin/utils/libutils.a)

set_source_files_properties(bzapi.i PROPERTIES CPLUSPLUS ON)
swig_add_library(bzapi TYPE SHARED LANGUAGE python SOURCES bzapi.i)
swig_link_libraries(bzapi
    ${BZAPI_LIBRARY}
    ${CRYPTO_LIBRARY}
    ${SWARM_LIBRARY}
    ${NODE_LIBRARY}
    ${DATABASE_LIBRARY}
    ${UTILS_LIBRARY}
    ${PROTO_LIBRARY}
    ${PROTOBUF_LIBRARIES}
    ${JSONCPP_LIBRARIES}
    ${OPENSSL_LIBRARIES}
    ${Boost_LIBRARIES}
    ${PYTHON_LIBRARIES})

set_target_properties(_bzapi PROPERTIES SUFFIX ".so")
add_dependencies(_bzapi bzapi_external)
