from nipype.pipeline import engine as pe
from nipype.interfaces import mrtrix3 as mrt
from nipype.interfaces import utility as niu

from ...interfaces import io

import os.path as op

def pop_template_wf(wdir=None, nthreads=1, name='population_template_wf'):
    """
    Set up population template workflow
    """

    # Define each node to use 4 cores if available
    if nthreads >= 4:
        nthreads = 4

    # Estimate group response for each tissue type
    avg_wm = pe.JoinNode(mrt.AverageResponse(), joinsource='SubjectID',
                                                joinfield=['in_files'],
                                                name='avgResponse_wm')
    avg_wm.base_dir = wdir
    avg_wm.inputs.out_file = 'avg_wm.txt'

    avg_gm = pe.JoinNode(mrt.AverageResponse(), joinsource='SubjectID',
                                                joinfield=['in_files'],
                                                name='avgResponse_gm')
    avg_gm.base_dir = wdir
    avg_gm.inputs.out_file = 'avg_gm.txt'

    avg_csf = pe.JoinNode(mrt.AverageResponse(), joinsource='SubjectID',
                                                 joinfield=['in_files'],
                                                 name='avgResponse_csf')
    avg_csf.base_dir = wdir
    avg_csf.inputs.out_file = 'avg_csf.txt'

    # dwi2fod
    dwi2fod = pe.MapNode(mrt.EstimateFOD(), iterfield=['in_file'],
                                            name='dwi2fod')
    dwi2fod.inputs.algorithm = 'msmt_csd'
    dwi2fod.inputs.nthreads = nthreads

    # Copy FOD and masks
    copyFOD = pe.JoinNode(niu.Function(function=io.copyFile,
                                       input_names=['in_file', 'out_dir'],
                                       output_names=['out_dir']),
                                       joinsource='SubjectID',
                                       joinfield=['in_file'],
                                       name='copyFOD')
    copyFOD.base_dir = wdir
    copyFOD.inputs.out_dir = op.join(copyFOD.base_dir + '/tmpFiles/FOD')

    copyMask = pe.JoinNode(niu.Function(function=io.copyFile,
                                        input_names=['in_file', 'out_dir'],
                                        output_names=['out_dir']),
                                        joinsource='SubjectID',
                                        joinfield=['in_file'],
                                        name='copyMask')
    copyMask.base_dir = wdir
    copyMask.inputs.out_dir = op.join(copyFOD.base_dir + '/tmpFiles/Mask')

    # Population template
    popTemplate = pe.Node(mrt.PopulationTemplate(), name='population_template')
    popTemplate.base_dir = wdir
    popTemplate.inputs.out_file = 'template_wmfod.mif'
    popTemplate.inputs.nthreads = nthreads
    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (avg_wm, dwi2fod, [('out_file', 'wm_txt')]),
        (avg_gm, dwi2fod, [('out_file', 'gm_txt')]),
        (avg_csf, dwi2fod, [('out_file', 'csf_txt')]),
        (dwi2fod, copyFOD, [('wm_odf', 'in_file')]),
        (copyFOD, popTemplate, [('out_dir', 'in_dir')]),
        (copyMask, popTemplate, [('out_dir', 'mask_dir')])
    ])

    return workflow
