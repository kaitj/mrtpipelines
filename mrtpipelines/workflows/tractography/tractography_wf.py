from nipype.pipeline import engine as pe
from nipype.interfaces import utility as niu
from nipype.interfaces import mrtrix3 as mrt

from ...interfaces import utils

import os.path as op

def genTemplate_wf(wdir=None, nthreads=1, name='genTemplate_wf'):
    """
    Set up workflow to generate template tracts
    """

    # Define nodes to use 4 cores if available
    if nthreads >= 4:
        nthreads = 4

    # Convert to VTK
    tempConvert1 = pe.MapNode(mrt.TCKConvert(), iterfield=['in_file'],
                                                name='tempConvert1')
    tempConvert1.base_dir = wdir
    tempConvert1.inputs.out_file = 'tracts.vtk'
    tempConvert1.inputs.nthreads = nthreads

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
                                           'tmpFiles/template_tract.vtk')

    # Convert to tck to select number of fibers
    tempConvert2 = pe.Node(mrt.TCKConvert(), name='tempConvert2')
    tempConvert2.base_dir = wdir
    tempConvert2.inputs.out_file = 'templateTracts.tck'
    tempConvert2.inputs.nthreads = nthreads

    # Select number of fibres for template
    tempSelect = pe.Node(mrt.TCKEdit(), name='tempSelect')
    tempSelect.base_dir = wdir
    tempSelect.inputs.number = 10000
    tempSelect.inputs.nthreads = nthreads

    # Convert template to vtk
    tempConvert3 = pe.Node(mrt.TCKConvert(), name='tempConvert3')
    tempConvert3.base_dir = wdir
    tempConvert3.inputs.out_file = 'templateTracts.vtk'
    tempConvert3.inputs.nthreads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (tempConvert1, genTemplate, [('out_file', 'in_tracts')]),
        (genTemplate, tempConvert2, [('out_tract', 'in_file')]),
        (tempConvert2, tempSelect, [('out_file', 'in_file')]),
        (tempSelect, tempConvert3, [('out_file', 'in_file')])
    ])

    return workflow

def genSubj_wf(nfibers=10000, wdir=None, nthreads=1, name='genSubj_wf'):
    """
    Set up workflow to generate subject tracts
    """

    # Define nodes to use 4 cores if available
    if nthreads >= 4:
        nthreads = 4

    # Subject select
    subjSelect = pe.MapNode(mrt.TCKEdit(), iterfield=['in_file'],
                                         name='subjSelect')
    subjSelect.base_dir = wdir
    subjSelect.inputs.number = nfibers
    subjSelect.nthreads = nthreads

    # Subject convert
    subjConvert = pe.MapNode(mrt.TCKConvert(), iterfield=['in_file'],
                                              name='subjConvert')
    subjConvert.base_dir = wdir
    subjConvert.inputs.out_file = 'subjectTracts.vtk'
    subjConvert.inputs.nthreads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (subjSelect, subjConvert, [('out_file', 'in_file')])
    ])

    return workflow
