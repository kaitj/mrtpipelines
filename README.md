# mrtpipelines

MRTrix3 processing to create a template using data collected as part of the
<sup>1</sup>[Human Connectome Project (HCP)](https://www.humanconnectome.org).

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
* genHCPURTemplate  
    * Performs template creation using 100 unrelated subjects of the [Human Connectome Project](https://www.humanconnectome.org) dataset. Templates are created based on available diffusion data with the <sup>2</sup>[MRTrix3](https://www.mrtrix.org) software. This pipeline creates the following templates:
        * Fiber Orientation Distribution (FOD)
        * Fractional Anisotropy (FA)
        * Mean Diffusivity (MD)
        * Axial Diffusivity (AD)
        * Radial Diffusivity (RD)
        * Diffusion Tensor
        * T1w
        * T2w

    <br>_Note that T1w and T2w images are made available for registration purposes when diffusion FODs may not be available._

### <a name="disclaimer"></a> Disclaimer
This branch of `mrtpipelines` is still undergoing development. While the pipeline can be used in its current state, it is possible for the project to undergo major changes.

Use of this branch is suited only for HCP datasets and is not currently suited for other datasets (please see [master branch](https://github.com/kaitj/mrtpipelines) for general-purpose use.

### <a name="install"></a> Installation
Development of this project was written in Python3 and makes use of [Nipype](https://github.com/nipy/nipype).

To install the package on your system, the following commands should be run:
```
git clone https://github.com/kaitj/mrtpipelines
git checkout HCP
pip install -r requirements.txt
python setup.py install
```

#### <a name="container"></a> Containerized package
This pipeline is also available within a Singularity container. Currently, users will have to build the container via the Singularity recipe found in the singularity directory of this repository. Future updates will look to implement and support Docker.

<strong>_It is highly advised to run this pipeline through the Singularity container. Some functionality may be lost if run locally due to custom additions to depedencies, which may yet to be implemented in original software._ <strong>

### <a name="usage"></a> Usage

Shown here is an example of the command line interface to run the pipeline:

```
Usage: genHCPURTemplate <bids dir> <subject list/subject id>
```

Or if running through singularity:

```
Usage: singularity exec <singularity_img> genHCPURTemplate <bids dir> <subject list/subject id>
```

#### <a name="reqargs"></a> Required arguments
```
bids_dir                Directory with input dataset,
                        formatted according to BIDS

participant_label       A file containing label(s) of
                        participant(s) to perform
                        pipeline execution on
```

#### <a name="optargs"></a> Optional arguments
```
-s      Number of streamlines to generate for each
        subject(s)

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
[1] D. C. Van Essen, S.M. Smith, D.M. Barch, T.E.J. Behrens, E. Yacoub, K. Ugurbil, for the WU-Minn HCP Consortium. (2013). The WU-Minn Human Connectome Project: An overview. NeuroImage 80(2013):62-79.

[2] J.-D. Tournier, F. Calamante, A. Connelly. MRtrix: Diffusion tractography in crossing fiber regions. Int J Imag Syst Tech 22(2012):53-66.
