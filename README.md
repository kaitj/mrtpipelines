# mrtpipelines

MRTrix3 processing for to create a template using data collected as part of the
[Human Connectome Project](https://www.humanconnectome.org).

## Contents
* [Available pipelines](#avail_pipelines)
* [Disclaimer](#disclaimer)
* [Support](#support)
* [References](#references)

### <a name="avail_pipelines"></a> Available pipelines
Details regarding usage and workflows coming soon...

* genHCPURTemplate  
    * Performs template creation using 100 unrelated subjects of the [Human Connectome Project](https://www.humanconnectome.org) dataset. Templates are created based on available diffusion data with the [MRTrix3](https://www.mrtrix.org) software. This pipeline creates the following templates:
        * Fiber Orientation Distribution (FOD)
        * Fractional Anisotropy (FA)
        * Mean Diffusivity (MD)
        * Axial Diffusivity (AD)
        * Radial Diffusivity (RD)
        * Diffusion Tensor
        * T1w
        * T2w

    Note that T1w and T2w images are made available for registration purposes when diffusion FODs may not be available.

### <a name="disclaimer"></a> Disclaimer
This branch of `mrtpipelines` is still in the development and may undergo major changes. Use of this branch is suited only for HCP datasets and is not currently suited for other datasets (please see [master branch](https://github.com/kaitj/mrtpipelines) for general-purpose use).

### <a name="support"></a> Support and communication
All bugs, concerns, and requests for features can be requested via the github repository found [here](https://github.com/kaitj/mrtpipelines/issues).

### <a name="references"></a> References
D. C. Van Essen, S.M. Smith, D.M. Barch, T.E.J. Behrens, E. Yacoub, K. Ugurbil, for the WU-Minn HCP Consortium. (2013). The WU-Minn Human Connectome Project: An overview. NeuroImage 80(2013):62-79.

J.-D. Tournier, F. Calamante, A. Connelly. MRtrix: Diffusion tractography in crossing fiber regions. Int J Imag Syst Tech 22(2012):53-66.
