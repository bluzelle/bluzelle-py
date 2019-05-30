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
          INSTALL_DIR bzapi_install
          CMAKE_ARGS "-DOMIT_LIBRARY=TRUE"
          INSTALL_COMMAND ""
          DOWNLOAD_COMMAND "")


add_definitions(-DBOOST_ERROR_CODE_HEADER_ONLY -DBOOST_LOG_DYN_LINK)
find_package(Boost     REQUIRED filesystem system log thread)
include_directories(${Boost_INCLUDE_DIRS})

include(FindPkgConfig)

pkg_search_module(JSONCPP REQUIRED jsoncpp)

include_directories(${JSONCPP_INCLUDE_DIRS})
link_directories(${JSONCPP_LIBRARY_DIRS})

include(FindProtobuf)
find_package(Protobuf REQUIRED)
include_directories(${PROTOBUF_INCLUDE_DIR})

# generated proto files
include_directories(${CMAKE_BINARY_DIR}/bzapi_bin)


find_package(PythonLibs 3 REQUIRED)

if(PYTHONLIBS_VERSION_STRING MATCHES "^2.*$" )
    set(CMAKE_SWIG_FLAGS -classic -c++)
else()
    set(CMAKE_SWIG_FLAGS -py3 -c++)
endif()

find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})


include_directories(${CMAKE_BINARY_DIR}/bzapi_bin/openssl/src/openssl-build/include)
include_directories(${CMAKE_BINARY_DIR}/bzapi_bin/openssl/src/openssl/include)
include_directories(${CMAKE_SOURCE_DIR}/bzapi)
include_directories(${CMAKE_SOURCE_DIR}/bzapi/include)

include_directories(${PYTHON_INCLUDE_DIRS})

set(CRYPTO_LIBRARIES ${CMAKE_BINARY_DIR}/bzapi_bin/crypto/libcrypto.a)
set(PROTO_LIBRARIES ${CMAKE_BINARY_DIR}/bzapi_bin/proto/libproto.a)
set(SWARM_LIBRARIES ${CMAKE_BINARY_DIR}/bzapi_bin/swarm/libswarm.a)
set(NODE_LIBRARIES ${CMAKE_BINARY_DIR}/bzapi_bin/node/libnode.a)
set(DATABASE_LIBRARIES ${CMAKE_BINARY_DIR}/bzapi_bin/database/libdatabase.a)
set(OPENSSL_LIBRARIES ${CMAKE_BINARY_DIR}/bzapi_bin/openssl/src/openssl-build/libcrypto.a ${CMAKE_BINARY_DIR}/bzapi_bin/openssl/src/openssl-build/libssl.a dl pthread)

set_source_files_properties(bzapi.i PROPERTIES CPLUSPLUS ON)
swig_add_library(bzapi TYPE SHARED LANGUAGE python SOURCES bzapi.i ${CMAKE_SOURCE_DIR}/bzapi/library/library.cpp ${CMAKE_SOURCE_DIR}/bzapi/include/bzapi.hpp ${CMAKE_SOURCE_DIR}/bzapi/include/response.hpp ${CMAKE_SOURCE_DIR}/bzapi/library/udp_response.hpp ${CMAKE_SOURCE_DIR}/bzapi/library/mutable_response.hpp ${CMAKE_SOURCE_DIR}/bzapi/include/logger.hpp ${CMAKE_SOURCE_DIR}/bzapi/library/log.cpp ${CMAKE_SOURCE_DIR}/bzapi/library/log.hpp)

swig_link_libraries(bzapi ${Boost_LOG_LIBRARIES} ${Boost_LIBRARIES} ${Boost_LOG_SETUP_LIBRARIES} ${PROTOBUF_LIBRARIES} ${JSONCPP_LIBRARIES} ${OPENSSL_LIBRARIES} ${CRYPTO_LIBRARIES} ${PROTO_LIBRARIES} ${SWARM_LIBRARIES} ${NODE_LIBRARIES} ${DATABASE_LIBRARIES} ${PYTHON_LIBRARIES})
set_target_properties(_bzapi PROPERTIES SUFFIX ".so")
add_dependencies(_bzapi bzapi_external)