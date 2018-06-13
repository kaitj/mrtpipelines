#!/bin/bash

# Dependencies
apt-get install -y g++ python python-numpy libeigen3-dev zlib1g-dev libqt4-opengl-dev libgl1-mesa-dev libfftw3-dev libtiff5-dev

# install mrtrix3
cd /opt/git
git clone https://github.com/MRtrix3/mrtrix3.git

cd mrtrix3
./configure
./build

# Setup
PROFILE=/.singularity.d/env/90-environment.sh
MRTRIX_HOME=/opt/git/mrtrix3

echo "" >> $PROFILE
echo "#mrtrix3" >> $PROFILE
echo "export PATH=$MRTRIX_HOME/bin/:\$PATH" >> $PROFILE
