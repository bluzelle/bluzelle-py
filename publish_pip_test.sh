#!/usr/bin/env bash
#
# *** Prereq ***
# 1) `git submodule update --remote` to get the latest bzapi c++ changes
# 2) change `version` in setup.py
#

#python3 setup.py sdist bdist_wheel
rm -rf dist .ccache bluzelle.egg-info
python3 setup.py sdist
python3 -m twine upload --skip-existing --repository testpypi dist/*