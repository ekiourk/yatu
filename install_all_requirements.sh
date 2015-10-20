#!/bin/bash

pip3 install -r acceptance/requirements.txt
pip3 install -r api/requirements.txt

cd base
python setup.py develop
cd -
