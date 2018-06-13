#!/bin/bash

# Install graphviz (for pipeline visual)
apt-get install -y graphviz

cd /opt/git

git clone https://github.com/kaitj/nipype
cd /opt/git/nipype
git checkout kai_dev

# Install requirements 
pip3 install -r requirements.txt

# Install custom nipype
python3 setup.py install
