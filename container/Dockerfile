FROM kaitj/mrtpipelines:base

MAINTAINER <tkai@uwo.ca>

run mkdir -p /src/install_scripts
COPY ./install_scripts/*.sh /src/install_scripts/

ENV DEBIAN_FRONTEND noninteractive
# RUN bash /src/install_scripts/00_install_basics.sh > log_00_basics
# RUN bash /src/install_scripts/01_install_freesurfer.sh > log_01_freesurfer
# RUN bash /src/install_scripts/02_install_mrtrix.sh > log_02_mrtrix
RUN bash /src/install_scripts/03b_install_mrtpipeline_template.sh > log_03_mrtpipeline_template
# RUN bash /src/install_scripts/04_install_nipype_custom.sh > log_04_nipype_custom

# Remove install scripts
RUN rm -rf /src

# Freesufer
# ENV FREESURFER_HOME /opt/freesurfer
# ENV PATH $FREESURFER_HOME/bin:$PATH

# Mrtrix
# ENV MRTRIX_HOME /opt/git/mrtrix3
# ENV PATH $MRTRIX_HOME/bin:$PATH
