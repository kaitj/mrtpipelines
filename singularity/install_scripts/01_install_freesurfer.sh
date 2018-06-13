#!/bin/basih

echo -n "Installing freesurfer ..."

S_DIR=/opt 
VERSION=6.0.0

mkdir -p $S_DIR/freesurfer

# Get freesurfer
wget ftp://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/${VERSION}/freesurfer-Linux-centos6_x86_64-stable-pub-v${VERSION}.tar.gz

tar -xvzf freesurfer-Linux-centos6_x86_64-stable-pub-v${VERSION}.tar.gz -C $S_DIR \
    --exclude='freesurfer/trctrain' \
    --exclude='freesurfer/subjects/fsaverage_sym' \
    --exclude='freesurfer/subjects/fsaverage3' \
    --exclude='freesurfer/subjects/fsaverage4' \
    --exclude='freesurfer/subjects/fsaverage5' \
    --exclude='freesurfer/subjects/fsaverage6' \
    --exclude='freesurfer/subjects/cvs_avg35' \
    --exclude='freesurfer/subjects/cvs_avg35_inMNI152' \
    --exclude='freesurfer/subjects/bert' \
    --exclude='freesurfer/subjects/V1_average' \
    --exclude='freesurfer/average/mult-comp-cor' \
    --exclude='freesurfer/lib/cuda' \
    --exclude='freesurfer/lib/qt'
rm freesurfer-Linux-centos6_x86_64-stable-pub-v${VERSION}.tar.gz 

# Get license
curl -L --retry 5 https://www.dropbox.com/s/38gghuq2w7h17pe/freesurfer_license -o $S_DIR/freesurfer/.license

# Setup

FREESURFER_HOME=$S_DIR/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh

#PROFILE=/environment
#FREESURFER_HOME=$S_DIR/freesurfer

#echo "" >> $PROFILE
#echo "#freesurfer" >> $PROFILE
#echo "export PATH=$FREESURFER_HOME/bin:\$PATH" >> $PROFILE
#echo "export $FREESURFER_HOME" >> $PROFILE

#source $PROFILE
