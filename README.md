# mrtpipelines

MRTrix3 processing diffusion and generating tractography of subject data from data collected.

## Contents
* [Introduction](#intro)
* [Disclaimer](#disclaimer)
* [Installation](#install)
    * [Containerized package](#container)
* [Usage](#usage)
    [Required arguments](#reqargs)
    [Optional arguments](#optargs)
* [Support](#support)
* [References](#references)

### <a name="intro"></a> Introduction
Details regarding usage and workflows coming soon.

* genACTTractography  
    * Performs preprocessing to generate anatomically constrained tractography. Assumes Freesurfer tissue segmentation available for ACT processing.
* genDhollanderTractography
    * Performs preprocessing to geneate whole-brain tractography following the Dhollander response algorithm.

_More information regarding algorithms used can be found from the <sup>1</sup>MRTrix3 website._

### <a name="disclaimer"></a> Disclaimer
This branch of `mrtpipelines` is still undergoing development. While the pipeline can be used in its current state, it is possible for the project to undergo major changes.

For HCP datasets, please see the [HCP branch](https://github.com/kaitj/mrtpipelines/tree/HCP).

### <a name="install"></a> Installation
Development of this project was written in Python3 and makes use of [Nipype](https://github.com/nipy/nipype).

To install the package on your system, the following commands should be run:
```
git clone https://github.com/kaitj/mrtpipelines
pip install -r requirements.txt
python setup.py install
```

#### <a name="container"></a> Containerized package
This pipeline is also available within a Singularity container. Currently, users will have to build the container via the Singularity recipe found in the singularity directory of this repository. Future updates will look to implement and support Docker.

<strong>_It is highly advised to run this pipeline through the Singularity container. Some functionality may be lost if run locally due to custom additions to depedencies, which may yet to be implemented in original software._</strong>

### <a name="usage"></a> Usage

Shown here is an example of the command line interface to run the pipeline:

```
Usage: genDhollanderTractography <bids dir> \
<template_fod> <subject list/subject id>
```

Or if running through singularity:

```
Usage: singularity exec <singularity_img> \
genDhollanderTractography <bids dir>  <template_fod> \
subject list/subject id>
```

#### <a name="reqargs"></a> Required arguments
```
bids_dir                Directory with input dataset,
                        formatted according to BIDS

template_fod            A path to the template FOD file
                        for registration of subjects

participant_label       A file containing label(s) of
                        participant(s) to perform
                        pipeline execution on
```
_Note there may be pipeline specific arguments if using a different tracking algorithm (eg. 5-tissue segmentation for ACT pipeline)_

#### <a name="optargs"></a> Optional arguments
```
-s      Number of streamlines to generate for each
        subject(s)

-l      Maxinum harmonic degree(s) for response
        function estimation (eg. -l 0 8 8)

-w      Work directory.
        Defaults to <bids_dir>/derivatives/MRTrix/work

-o      Output directory.
        Defaults to <bids_dir>/derivatives/MRTrix/out

-n      Number of threads to use for pipeline execution
        where applicable

-h      Display help documentation
```


### <a name="support"></a> Support and communication

All bugs, concerns, and requests for features can be requested via the github repository found [here](https://github.com/kaitj/mrtpipelines/issues).

### <a name="references"></a> References
[1] J.-D. Tournier, F. Calamante, A. Connelly. MRtrix: Diffusion tractography in crossing fiber regions. Int J Imag Syst Tech 22(2012):53-66.
