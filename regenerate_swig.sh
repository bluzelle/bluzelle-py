#!/usr/bin/env bash

ROOT=$(pwd)
TMP_DIR=$ROOT/publish
rm -rf $TMP_DIR && mkdir $TMP_DIR
cp -r $ROOT/bluzelle $ROOT/setup.cfg $ROOT/setup.py $ROOT/requirements.txt $ROOT/LICENSE $ROOT/MANIFEST.in $ROOT/README.md $ROOT/dummy.c $TMP_DIR

BUILD_DIR=$TMP_DIR/bluzelle/bzpy/build
rm -rf $BUILD_DIR && mkdir -p $BUILD_DIR 2>/dev/null
cd $BUILD_DIR
cmake $TMP_DIR/bluzelle/bzpy
cmake --build $BUILD_DIR -- -j4
cp $BUILD_DIR/_bzapi.so $ROOT/bluzelle
cp $BUILD_DIR/bzapi.py $ROOT/bluzelle

cd $ROOT
rm -rf $TMP_DIR