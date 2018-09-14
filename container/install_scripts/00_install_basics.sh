#!/bin/bash

apt-get update

apt-get install -y --no-install-recommends apt-utils

#basic
apt-get install -y sudo wget curl git dos2unix tree zip unzip vim dc

#
apt-get install -y make cmake

# python & pip3 
apt-get install -y python3 python3.5-dev
curl https://bootstrap.pypa.io/get-pip.py | python3

# freesurfer
apt-get install -y tcsh
apt-get install -y libqt4-scripttools libqt4-dev libjpeg62 libxss1 libxft2
