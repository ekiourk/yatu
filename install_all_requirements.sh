#!/bin/bash

pip3 install -r tests/requirements.txt
pip3 install -r api/requirements.txt

cd base
python setup.py develop
cd -
