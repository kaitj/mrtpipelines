#!/bin/bash

cd /opt/git
git clone https://github.com/kaitj/mrtpipelines

cd /opt/git/mrtpipelines

# Install requirements
pip3 install -r requirements.txt

# Install mrtpipelines
python3 setup.py install
