from nipype.pipeline import engine as pe
from nipype.interfaces import utility as niu
from nipype.interfaces import mrtrix3 as mrt

from ...interfaces import utils

import os.path as op

def genTemplate_wf(nfibers=7500, wdir=None, nthreads=1, name='genTemplate_wf'):
    """
    Set up workflow to generate template tracts
    """

    # Define nodes to use 4 cores if available
    if nthreads >= 4:
        nthreads = 4

    # Generate subject tracts for template creation
    genSubjTemp = pe.MapNode(mrt.Tractography(), iterfield=['in_file',
                                                            'act_file',
                                                            'seed_gmwmi'],
                                                 name='genSubjTemp')
    genSubjTemp.base_dir = wdir
    genSubjTemp.inputs.max_length = 200
    genSubjTemp.inputs.power = 1
    genSubjTemp.inputs.backtrack
    genSubjTemp.inputs.n_tracks = int(nfibers * 2)
    genSubjTemp.nthreads = nthreads

    # SIFT (Spherical-deconvolution informed filtering of tractograms)
    sift = pe.MapNode(mrt.SIFT(), iterfield=['in_file', 'in_fod'],
                                  name='siftTemplate')
    sift.base_dir = wdir
    sift.term_number = nfibers
    sift.nthreads = nthreads

    # Convert to VTK
    tempConvert = pe.MapNode(mrt.TCKConvert(), iterfield=['in_file'],
                                               name='template2vtk')
    tempConvert.base_dir = wdir
    tempConvert.inputs.out_file = 'tracts_filtered.vtk'
    tempConvert.nthreads = nthreads

    # Craete template tract
    genTemplate = pe.JoinNode(niu.Function(function=utils.createTemplateTract,
                                           input_names=['in_tracts',
                                                        'out_tract'],
                                           output_names=['out_tract']),
                                           joinsource='SubjectID',
                                           joinfield=['in_tracts'],
                                           name='genTemplate')
    genTemplate.base_dir = wdir
    genTemplate.inputs.out_tract = op.join(genTemplate.base_dir,
                                           'tmpFiles/template_tract.tck')

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (genSubjTemp, sift, [('out_file', 'in_file')]),
        (sift, tempConvert, [('out_file', 'in_file')]),
        (tempConvert, genTemplate, [('out_file', 'in_tracts')])
    ])

    return workflow

def genSubj_wf(nfibers=100000, wdir=None, nthreads=1, name='genSubj_wf'):
    """
    Set up workflow to generate subject tracts
    """

    # Define nodes to use 4 cores if available
    if nthreads >= 4:
        nthreads = 4

    # Generate subject tracts
    genSubjTracts = pe.MapNode(mrt.Tractography(), iterfield=['in_file',
                                                            'act_file',
                                                            'seed_gmwmi'],
                                                name='genSubjTracts')
    genSubjTracts.base_dir = wdir
    genSubjTracts.inputs.max_length = 200
    genSubjTracts.inputs.power = 1
    genSubjTracts.inputs.backtrack
    genSubjTracts.inputs.n_tracks = int(nfibers * 2)
    genSubjTracts.nthreads = nthreads

    # SIFT (Spherical-deconvolution informated filtering of tractograms)
    sift = pe.MapNode(mrt.SIFT(), iterfield=['in_file', 'in_fod'],
                                  name='siftSubject')
    sift.base_dir = wdir
    sift.term_number = nfibers
    sift.nthreads = nthreads

    # Convert to VTK
    subjConvert = pe.MapNode(mrt.TCKConvert(), iterfield=['in_file'],
                                               name='subject2vtk')
    subjConvert.base_dir = wdir
    subjConvert.inputs.out_file = 'tracts_filtered.vtk'
    subjConvert.nthreads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (genSubjTracts, sift, [('out_file', 'in_file')]),
        (sift, subjConvert, [('out_file', 'in_file')]),
    ])

    return workflow
