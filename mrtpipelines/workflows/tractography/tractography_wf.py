from nipype.pipeline import engine as pe
from nipype.interfaces import utility as niu
from nipype.interfaces import mrtrix3 as mrt

from ...interfaces import utils

import os.path as op

def genTemplate_wf(wdir=None, nthreads=1, name='genTemplateTract_wf'):
    """
    Set up workflow to generate Tractography
    """

    # Register subjects to template
    # Generate tractography
    genTract = pe.Node(mrt.Tractography(), name='template_tckgen')
    genTract.base_dir = wdir
    genTract.inputs.backtrack
    genTract.inputs.n_tracks = 1000000
    genTract.inputs.out_file = 'template_variant-tckgen_streamlines-1M_tract.tck'
    genTract.inputs.nthreads = nthreads

    # Sphereical-deconvoulution informed filtering of tractography
    siftTract = pe.Node(mrt.SIFT(), name='template_tcksift')
    siftTract.base_dir = wdir
    siftTract.inputs.term_number = 500000
    siftTract.inputs.out_file = 'template_variant-sift_streamlines-500K_tract.tck'
    siftTract.inputs.nthreads = nthreads

    tractConvert = pe.Node(mrt.TCKConvert(), name='template_tckconvert')
    tractConvert.base_dir = wdir
    tractConvert.inputs.out_file = 'template_variant_sift_streamlines-500K_tract.vtk'
    tractConvert.inputs.nthreads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (genTract, siftTract, [('out_file', 'in_file')]),
        (siftTract, tractConvert, [('out_file', 'in_file')])
    ])

    return workflow


def genSubj_wf(nfibers=100000, wdir=None, nthreads=1, name='genSubj_wf'):
    """
    Set up workflow to generate subject tracts
    """

    # Subject select
    subjSelect = pe.MapNode(mrt.TCKEdit(), iterfield=['in_file'],
                                         name='subjSelect')
    subjSelect.base_dir = wdir
    subjSelect.inputs.number = nfibers
    subjSelect.inputs.out_file = 'space-Template_variant-sift_streamlines_%d_tract.tck' % nfibers
    subjSelect.nthreads = nthreads

    # Subject convert
    subjConvert = pe.MapNode(mrt.TCKConvert(), iterfield=['in_file'],
                                              name='subjConvert')
    subjConvert.base_dir = wdir
    subjConvert.inputs.out_file = 'space-Template_variant-sift_streamlines_%d_tract.vtk' % nfibers
    subjConvert.inputs.nthreads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (subjSelect, subjConvert, [('out_file', 'in_file')])
    ])

    return workflow
