import os
import setuptools
from setuptools.extension import Extension
import subprocess
from pprint import pprint
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()


this_dir = os.path.dirname(os.path.abspath(__file__))

from distutils.command.install_data import install_data
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install_lib import install_lib
from setuptools.command.install_scripts import install_scripts
from setuptools.command.develop import develop
from setuptools.command.install import install
import site


from setuptools.command.build_ext import build_ext as build_ext_orig

import struct
import shutil
import pathlib
import platform

# taken from https://stackoverflow.com/questions/42585210/extending-setuptools-extension-to-use-cmake-in-setup-py
class CMakeExtension(Extension):

    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])


class build_ext(build_ext_orig):

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        cwd = pathlib.Path().absolute()
        bzpy_path = str(cwd) + "/bluzelle/bzpy"

        # these dirs will be created in build_py, so if you don't have
        # any python sources to bundle, the dirs will be missing
        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
        extdir.mkdir(parents=True, exist_ok=True)

        # example of cmake args
        config = 'Debug' if self.debug else 'Release'
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + str(extdir.parent.absolute()),
            '-DCMAKE_BUILD_TYPE=' + config,
            '-DBZAPI_PATH='+bzpy_path+'/bzapi',
        ]

        # example of build args
        build_args = [
            '--config', config,
            '--', '-j4'
        ]

        os.chdir(str(build_temp))
        folders = []

        # r=root, d=directories, f = files
        for r, d, f in os.walk(str(cwd)):
            for folder in d:
                folders.append(os.path.join(r, folder))

        for f in folders:
            print(f)


        self.spawn(['cmake', str(bzpy_path)] + cmake_args)

        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'] + build_args)

        os.chdir(str(cwd))

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        install.run(self)

setuptools.setup(
    name="bluzelle",
    # Updated via travisd: https://travis-ci.org/guettli/reprec
    # See .travis.yml
    version="0.10.7",
    author="Yarco Hayduk",
    author_email="yaroslav@bluzelle.com",
    description="A Python Bluzelle client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yarco/bluzelle",
    packages=setuptools.find_packages(),
    #package_data={'bluzelle': ['bluzelle/bzapi', 'bluzelle/_bzapi.so', 'bluzelle/libbzapi.dylib','bluzelle/libjsoncpp.so.19', 'bluzelle/libbzapi.so', 'tests/tests.py']},
    #   package_dir = {'bluzelle/bzapi'},
    include_package_data=True,
    install_requires=[
          'ecdsa',
    ],
    # This distribution contains platform-specific C++ libraries, but they are not
    # built with distutils. So we must create a dummy Extension object so when we
    # create a binary file it knows to make it platform-specific.
    #ext_modules=[Extension('Bluzelle.dummy', sources = ['dummy.c'])],
    ext_modules=[CMakeExtension('bzpy')],
    cmdclass={
        'install': PostInstallCommand,
        'build_ext': build_ext,
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)