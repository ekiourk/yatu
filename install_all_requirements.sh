#!/bin/bash

pip3 install -r apps/acceptance/requirements.txt
pip3 install -r apps/api/requirements.txt

cd apps/base
python setup.py develop
cd -
