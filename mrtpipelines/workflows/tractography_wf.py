from nipype.pipeline import engine as pe
from nipype.interfaces import mrtrix3 as mrt

import numpy as np

def genDhollTract_wf(nfibers=50000, sshell=False, wdir=None, nthreads=1,
                     name='genDhollTract_wf'):
    """
    Set up workflow to generate tracts with Dhollander response
    """

    # Generate tract
    genTract = pe.Node(mrt.Tractography(), name='genTract')
    genTract.base_dir = wdir
    genTract.inputs.n_tracks = np.int(nfibers * 2)
    if sshell is False:  # Single-shell
        genTract.inputs.out_file = 'space-Template_desc-iFOD2_tractography.tck'
        genTract.inputs.algorithm = 'iFOD2'
    else:
        genTract.inputs.out_file = 'space-Template_desc-TensorProb_tractography.tck'
        genTract.inputs.algorithm = 'Tensor_Prob'
    genTract.inputs.nthreads = nthreads
    genTract.interface.num_threads = nthreads

    # Spherical-deconvolution informed filtering of tractography
    siftTract = pe.Node(mrt.SIFT(), name='siftTract')
    siftTract.base_dir = wdir
    siftTract.inputs.term_number = nfibers
    if sshell is False:  # Multi-shell
        siftTract.inputs.out_file = 'space-Template_desc-iFOD2_tractography.tck'
    else:  # Single-shell
        siftTract.inputs.out_file = 'space-Template_desc-TensorProb_tractography.tck'
    siftTract.inputs.nthreads = nthreads
    siftTract.interface.num_threads = nthreads

    # Convert to VTK
    tractConvert = pe.Node(mrt.TCKConvert(), name='convTract')
    tractConvert.base_dir = wdir
    if sshell is False:  # Multi-shell
        tractConvert.inputs.out_file = 'space-Template_desc-iFOD2_tractography.vtk'
    else:  # Single-shell
        tractConvert.inputs.out_file = 'space-Template_desc-TensorProb_tractography.vtk'
    tractConvert.inputs.nthreads = nthreads
    tractConvert.interface.num_threads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (genTract, siftTract, [('out_file', 'in_file')]),
        (siftTract, tractConvert, [('out_file', 'in_file')])
    ])

    return workflow
