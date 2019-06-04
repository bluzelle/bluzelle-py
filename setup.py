import os
import setuptools
import shutil
import pathlib

from setuptools import Extension
from setuptools.command.install import install
from distutils.command.build import build

with open("README.md", "r") as fh:
    long_description = fh.read()

this_dir = os.path.dirname(os.path.abspath(__file__))

from setuptools.command.build_ext import build_ext as build_ext_orig

# from https://stackoverflow.com/questions/12491328/python-distutils-not-include-the-swig-generated-module
# Need to redefine these so that we can include the swig-generated files inside of the `bluzelle` folder
class CustomBuild(build):
    def run(self):
        self.run_command('build_ext')
        build.run(self)


class CustomInstall(install):
    def run(self):
        self.run_command('build_ext')
        install.run(self)


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

        # these dirs will be created in build_py
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

        self.spawn(['cmake', str(bzpy_path)] + cmake_args)

        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'] + build_args)

        # copy the generated python wrapper to the root of bluzelle
        shutil.copyfile('bzapi.py', str(cwd) + "/bluzelle/bzapi.py")

        os.chdir(str(cwd))


setuptools.setup(
    name="bluzelle",
    version="0.58.0",
    author="Yarco Hayduk",
    author_email="yaroslav@bluzelle.com",
    description="A Python Bluzelle client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yarco/bluzelle",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
          'ecdsa',
    ],
    # *** this part is for building wheels in the future ***
    # This distribution contains platform-specific C++ libraries, but they are not
    # built with distutils. So we must create a dummy Extension object so when we
    # create a binary file it knows to make it platform-specific.
    # ext_modules=[Extension('Bluzelle.dummy', sources = ['dummy.c'])],
    # package_data={'bluzelle': ['bluzelle/bzapi', 'bluzelle/_bzapi.so', 'bluzelle/libbzapi.dylib','bluzelle/libjsoncpp.so.19', 'bluzelle/libbzapi.so', 'tests/tests.py']},
    # package_dir = {'bluzelle/bzapi'},
    # *** ---------------------------------------------- ***

    ext_modules=[CMakeExtension('bzpy')],
    py_modules = ['bzpy'],
    cmdclass={'build_ext': build_ext, 'build': CustomBuild, 'install': CustomInstall},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)