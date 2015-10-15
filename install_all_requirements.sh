#!/bin/bash

pip3 install -r apps/acceptance/requirements.txt
pip3 install -r apps/api/requirements.txt

python apps/base/setup.py develop