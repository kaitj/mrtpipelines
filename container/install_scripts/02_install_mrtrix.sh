#!/bin/bash

DIR=/opt/git

mkdir -p $DIR/mrtrix3

# Dependencies
apt-get install -y g++ python python-numpy libeigen3-dev zlib1g-dev libqt4-opengl-dev libgl1-mesa-dev libfftw3-dev libtiff5-dev

# install mrtrix3
git clone https://github.com/MRtrix3/mrtrix3.git $DIR/mrtrix3

cd $DIR/mrtrix3
./configure
./build

# Setup
#PROFILE=/environment
#MRTRIX_HOME=$HOME/mrtrix3

#echo "" >> $PROFILE
#echo "#mrtrix3" >> $PROFILE
#echo "export PATH=$MRTRIX_HOME/bin/:\$PATH" >> $PROFILE

#source $PROFILE
