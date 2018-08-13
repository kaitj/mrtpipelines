from nipype.pipeline import engine as pe
from nipype.interfaces import mrtrix3 as mrt

import numpy as np

def genTract_wf(nfibers=25000, wdir=None, nthreads=1,
                name='genTract_wf'):
    """
    Set up workflow to generate tracts
    """

    # Define number of threads to use
    if nthreads >= 8:
        nthreads = np.int(nthreads / 4)

    # Generate tract
    genTract = pe.Node(mrt.Tractography(), name='genTract')
    genTract.base_dir = wdir
    genTract.inputs.backtrack
    genTract.inputs.n_tracks = np.int(nfibers * 2)
    genTract.inputs.out_file = 'variant-tckgen_streamlines-%d_tract.tck' % (np.int(nfibers*2))
    genTract.inputs.nthreads = nthreads
    genTract.interface.num_threads = nthreads

    # Spherical-deconvolution informed filtering of tractography
    siftTract = pe.Node(mrt.Tractography(), name='siftTract')
    siftTract.base_dir = wdir
    siftTract.inputs.term_number = nfibers
    siftTract.inputs.out_File = 'variant-tcksift_streamlines-%d_tract.tck' % nfibers
    siftTract.inputs.nthreads = nthreads
    siftTract.interface.num_threads = nthreads

    # Convert to VTK
    tractConvert = pe.Node(mrt.TCKConvert(), name='convTract')
    tractConvert.base_dir = wdir
    tractConvert.inputs.out_file = 'variant-tcksift_streamlines-%d_tract.vtk' % nfibers
    tractConvert.inputs.nthreads = nthreads
    tractConvert.interface.num_threads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (genTract, siftTract, [('out_file', 'in_file')]),
        (siftTract, tractConvert, [('out_file', 'in_file')])
    ])

    return workflow
