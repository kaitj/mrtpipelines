#!/bin/bash

DIR=/opt/git/
mkdir -p $DIR/mrtpipelines

# Git
git clone https://github.com/kaitj/mrtpipelines $DIR/mrtpipelines
cd $DIR/mrtpipelines
git checkout template

# Install requirements
pip3 install -r requirements.txt

# Install mrtpipelines
python3 setup.py install
