from nipype.pipeline import engine as pe
from nipype.interfaces import mrtrix3 as mrt
from nipype.interfaces import utility as niu

from ..interfaces import io, utils

import os.path as op
import numpy as np

def fodTemplate_wf(wdir=None, nthreads=1, name='fodTemplate_wf'):
    """
    Set up population fod template workflow
    """

    if nthreads >= 8:
        int_nthreads = np.int(nthreads / 4)
    else:
        int_nthreads = nthreads

    # Estimate group response for each tissue type
    avg_wm = pe.JoinNode(mrt.AverageResponse(), joinsource='SubjectID',
                                                joinfield=['in_files'],
                                                name='avgResponse_wm')
    avg_wm.base_dir = wdir
    avg_wm.inputs.out_file = 'template_wmresponse.txt'
    avg_wm.interface.num_threads = nthreads

    avg_gm = pe.JoinNode(mrt.AverageResponse(), joinsource='SubjectID',
                                                joinfield=['in_files'],
                                                name='avgResponse_gm')
    avg_gm.base_dir = wdir
    avg_gm.inputs.out_file = 'template_gmresponse.txt'
    avg_gm.interface.num_threads = nthreads

    avg_csf = pe.JoinNode(mrt.AverageResponse(), joinsource='SubjectID',
                                                 joinfield=['in_files'],
                                                 name='avgResponse_csf')
    avg_csf.base_dir = wdir
    avg_csf.inputs.out_file = 'template_csfresponse.txt'
    avg_csf.interface.num_threads = nthreads

    # dwi2fod
    dwi2fod = pe.MapNode(mrt.EstimateFOD(), iterfield=['in_file'],
                                            name='dwi2fod')
    dwi2fod.base_dir = wdir
    dwi2fod.inputs.algorithm = 'msmt_csd'
    dwi2fod.inputs.nthreads = int_nthreads
    dwi2fod.interface.num_threads = int_nthreads

    # mtnormalise
    mtnormalise = pe.MapNode(mrt.MTNormalise(), iterfield=['in_wm',
                                                           'in_gm',
                                                           'in_csf',
                                                           'mask'],
                                                name='mtnormalise')
    mtnormalise.base_dir = wdir
    mtnormalise.inputs.nthreads = int_nthreads
    mtnormalise.interface.num_threads = int_nthreads

    # Copy FOD and masks
    copyFOD = pe.JoinNode(niu.Function(function=io.copyFile,
                                       input_names=['in_file', 'out_dir'],
                                       output_names=['out_dir']),
                                       joinsource='SubjectID',
                                       joinfield=['in_file'],
                                       name='copyFOD')
    copyFOD.base_dir = wdir
    copyFOD.inputs.out_dir = op.join(copyFOD.base_dir + '/tmpFiles/FOD')
    copyFOD.interface.num_threads = nthreads

    copyMask = pe.JoinNode(niu.Function(function=io.copyFile,
                                        input_names=['in_file', 'out_dir'],
                                        output_names=['out_dir']),
                                        joinsource='SubjectID',
                                        joinfield=['in_file'],
                                        name='copyMask')
    copyMask.base_dir = wdir
    copyMask.inputs.out_dir = op.join(copyFOD.base_dir + '/tmpFiles/Mask')
    copyMask.interface.num_threads = nthreads

    # Population template
    FODTemplate = pe.Node(mrt.PopulationTemplate(), name='FODTemplate')
    FODTemplate.base_dir = wdir
    FODTemplate.inputs.out_file = 'template_wmfod.mif'
    FODTemplate.inputs.nthreads = nthreads
    FODTemplate.interface.num_threads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (avg_wm, dwi2fod, [('out_file', 'wm_txt')]),
        (avg_gm, dwi2fod, [('out_file', 'gm_txt')]),
        (avg_csf, dwi2fod, [('out_file', 'csf_txt')]),
        (dwi2fod, mtnormalise, [('wm_odf', 'in_wm'),
                                ('gm_odf', 'in_gm'),
                                ('csf_odf', 'in_csf')]),
        (mtnormalise, copyFOD, [('out_wm', 'in_file')]),
        (copyFOD, FODTemplate, [('out_dir', 'in_dir')]),
        (copyMask, FODTemplate, [('out_dir', 'mask_dir')])
    ])

    return workflow


def tensorTemplate_wf(wdir=None, nthreads=1, name='tensorTemplate_wf'):
    """
    Set up population tensor template workflow
    """

    # Copy nodes for necessary files
    copyFA = pe.JoinNode(niu.Function(function=io.copyFile,
                                      input_namefixels=['in_file', 'out_dir'],
                                      output_names=['out_dir']),
                                      joinsource='SubjectID',
                                      joinfield=['in_file'],
                                      name='copyFA')
    copyFA.base_dir = wdir
    copyFA.inputs.out_dir = op.join(copyFA.base_dir + '/tmpFiles/FA')
    copyFA.interface.num_threads = nthreads

    copyMD = pe.JoinNode(niu.Function(function=io.copyFile,
                                      input_names=['in_file', 'out_dir'],
                                      output_names=['out_dir']),
                                      joinsource='SubjectID',
                                      joinfield=['in_file'],
                                      name='copyMD')
    copyMD.base_dir = wdir
    copyMD.inputs.out_dir = op.join(copyMD.base_dir + '/tmpFiles/MD')
    copyMD.interface.num_threads = nthreads

    copyAD = pe.JoinNode(niu.Function(function=io.copyFile,
                                      input_names=['in_file', 'out_dir'],
                                      output_names=['out_dir']),
                                      joinsource='SubjectID',
                                      joinfield=['in_file'],
                                      name='copyAD')
    copyAD.base_dir = wdir
    copyAD.inputs.out_dir = op.join(copyAD.base_dir + '/tmpFiles/AD')
    copyAD.interface.num_threads = nthreads

    copyRD = pe.JoinNode(niu.Function(function=io.copyFile,
                                      input_names=['in_file', 'out_dir'],
                                      output_names=['out_dir']),
                                      joinsource='SubjectID',
                                      joinfield=['in_file'],
                                      name='copyRD')
    copyRD.base_dir = wdir
    copyRD.inputs.out_dir = op.join(copyRD.base_dir + '/tmpFiles/RD')
    copyRD.interface.num_threads = nthreads

    copyTempMask = pe.JoinNode(niu.Function(function=io.copyFile,
                                            input_names=['in_file', 'out_dir'],
                                            output_names=['out_dir']),
                                            joinsource='SubjectID',
                                            joinfield=['in_file'],
                                            name='copyTempMask')
    copyTempMask.base_dir = wdir
    copyTempMask.inputs.out_dir = op.join(copyTempMask.base_dir +
                                          '/tmpFiles/TempMask')
    copyTempMask.interface.num_threads = nthreads

    # Population template
    FATemplate = pe.Node(mrt.PopulationTemplate(), name='FATemplate')
    FATemplate.base_dir = wdir
    FATemplate.inputs.out_file = 'template_fa.mif'
    FATemplate.inputs.nthreads = nthreads
    FATemplate.interface.num_threads = nthreads

    MDTemplate = pe.Node(mrt.PopulationTemplate(), name='MDTemplate')
    MDTemplate.base_dir = wdir
    MDTemplate.inputs.out_file = 'template_md.mif'
    MDTemplate.inputs.nthreads = nthreads
    MDTemplate.interface.num_threads = nthreads

    ADTemplate = pe.Node(mrt.PopulationTemplate(), name='ADTemplate')
    ADTemplate.base_dir = wdir
    ADTemplate.inputs.out_file = 'template_ad.mif'
    ADTemplate.inputs.nthreads = nthreads
    ADTemplate.interface.num_threads = nthreads

    RDTemplate = pe.Node(mrt.PopulationTemplate(), name='RDTemplate')
    RDTemplate.base_dir = wdir
    RDTemplate.inputs.out_file = 'template_rd.mif'
    RDTemplate.inputs.nthreads = nthreads
    RDTemplate.interface.num_threads = nthreads

    # Template mask
    selectMasks = pe.Node(niu.Function(function=utils.selectAll,
                                       input_names=['in_dir'],
                                       output_names=['out_files']),
                                       name='selectMasks')
    selectMasks.base_dir = wdir
    selectMasks.interface.num_threads = nthreads

    MaskTemplate = pe.Node(mrt.MRMath(), name='MaskTemplate')
    MaskTemplate.base_dir = wdir
    MaskTemplate.inputs.out_file = 'template_brainmask.mif'
    MaskTemplate.inputs.operation ='min'
    MaskTemplate.inputs.nthreads = nthreads
    MaskTemplate.interface.num_threads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (copyFA, FATemplate, [('out_dir', 'in_dir')]),
        (copyTempMask, FATemplate, [('out_dir', 'mask_dir')]),
        (copyMD, MDTemplate, [('out_dir', 'in_dir')]),
        (copyTempMask, MDTemplate, [('out_dir', 'mask_dir')]),
        (copyAD, ADTemplate, [('out_dir', 'in_dir')]),
        (copyTempMask, ADTemplate, [('out_dir', 'mask_dir')]),
        (copyRD, RDTemplate, [('out_dir', 'in_dir')]),
        (copyTempMask, RDTemplate, [('out_dir', 'mask_dir')]),
        (copyTempMask, selectMasks, [('out_dir', 'in_dir')]),
        (selectMasks, MaskTemplate, [('out_files', 'in_file')])
    ])

    return workflow


def anatTemplate_wf(wdir=None, nthreads=1, name='anatTemplate_wf'):
    """
    Set up population template anatomical workflow
    """

    if nthreads >= 8:
        nthreads = np.int(nthreads / 4)

    # Copy nodes
    copyT1w = pe.JoinNode(niu.Function(function=io.copyFile,
                                       input_namefixels=['in_file', 'out_dir'],
                                       output_names=['out_dir']),
                                       joinsource='SubjectID',
                                       joinfield=['in_file'],
                                       name='copyT1w')
    copyT1w.base_dir = wdir
    copyT1w.inputs.out_dir = op.join(copyT1w.base_dir + '/tmpFiles/T1w')
    copyT1w.interface.num_threads = nthreads

    copyT2w = pe.JoinNode(niu.Function(function=io.copyFile,
                                       input_namefixels=['in_file', 'out_dir'],
                                       output_names=['out_dir']),
                                       joinsource='SubjectID',
                                       joinfield=['in_file'],
                                       name='copyT2w')
    copyT2w.base_dir = wdir
    copyT2w.inputs.out_dir = op.join(copyT1w.base_dir + '/tmpFiles/T2w')
    copyT2w.interface.num_threads = nthreads

    # Template nodes
    T1wTemplate = pe.Node(mrt.PopulationTemplate(), name='T1wTemplate')
    T1wTemplate.base_dir = wdir
    T1wTemplate.inputs.out_file = 'template_t1w.mif'
    T1wTemplate.inputs.nthreads = nthreads
    T1wTemplate.interface.num_threads = nthreads

    T2wTemplate = pe.Node(mrt.PopulationTemplate(), name='T2wTemplate')
    T2wTemplate.base_dir = wdir
    T2wTemplate.inputs.out_file = 'template_t2w.mif'
    T2wTemplate.inputs.nthreads = nthreads
    T2wTemplate.interface.num_threads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (copyT1w, T1wTemplate, [('out_dir', 'in_dir')]),
        (copyT2w, T2wTemplate, [('out_dir', 'in_dir')])
    ])

    return workflow
