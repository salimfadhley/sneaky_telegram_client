#!/bin/bash
python3.8 -m venv ./venv
. ./venv/bin/activate
python -m pip install wheel
cd src
ls -l
python -m pip install .
