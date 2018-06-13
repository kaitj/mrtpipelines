#!/bin/bash

# Install graphviz (for pipeline visual)
apt-get install -y graphviz

# Git
DIR=/opt/git
mkdir -p $DIR/nipype

git clone https://github.com/kaitj/nipype $DIR/nipype
cd $DIR/nipype
git checkout kai_dev

# Install requirements 
pip3 install -r requirements.txt

# Install custom nipype
python3 setup.py install
