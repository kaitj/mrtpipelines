from nipype import IdentityInterface
from nipype.pipeline import engine as pe

import numpy as np
import os.path as op

def getSubj(subjFile, work_dir, nthreads=1):
    # Retrieve individual subject ids & number of subjectss
    subjids = []
    noSubj = 0
    with open(subjFile) as f:
        for subj in f:
            # temp = subj.lstrip('sub-')
            temp = subj.rstrip('\n')
            subjids.append(temp)
            noSubj += 1

    Subjid = pe.Node(IdentityInterface(fields=['subjid']), name='SubjectID')
    Subjid.base_dir = work_dir
    Subjid.iterables = [('subjid', subjids)]
    Subjid.interface.num_threads = nthreads

    return Subjid, noSubj


def _getTemplate(template_dir, template_label, work_dir):
    tempdir = op.abspath(op.join(template_dir, 'response'))

    wm_fod = template_label + '_wmfod.mif'
    wm_fod = op.join(tempdir, wm_fod)
    wm_response = template_label + '_wmresponse.txt'
    wm_response = op.join(tempdir, wm_response)
    gm_response = template_label + '_gmresponse.txt'
    gm_response = op.join(tempdir, gm_response)
    csf_response = template_label + '_csfresponse.txt'
    csf_response = op.join(tempdir, csf_response)

    return wm_fod, wm_response, gm_response, csf_response

def getTemplate(template_dir, template_label, wdir=None):
    from nipype.pipeline import engine as pe
    from nipype.interfaces import utility as niu

    from mrtpipelines.interfaces import io

    getTemplate = pe.Node(niu.Function(function=io._getTemplate,
                                        input_names=['template_dir',
                                                     'template_label',
                                                     'work_dir'],
                                        output_names=['wm_fod',
                                                      'wm_response',
                                                      'gm_response',
                                                      'csf_response']),
                                        name='getTemplate')

    getTemplate.base_dir = wdir
    getTemplate.inputs.template_dir = template_dir
    getTemplate.inputs.template_label = template_label
    getTemplate.inputs.work_dir = wdir

    return getTemplate


def _getData(bids_layout, subjid):
    # Strip leading 'sub-'
    subjid = subjid.lstrip('sub-')

    # Diffusion
    nifti = bids_layout.get(subject=subjid, modality='dwi', type='preproc',
                            return_type='file', extensions=['nii', 'nii.gz'])
    bval = bids_layout.get(subject=subjid, modality='dwi', type='preproc',
                           return_type='file', extensions=['bval'])
    bvec = bids_layout.get(subject=subjid, modality='dwi', type='preproc',
                           return_type='file', extensions=['bvec'])
    mask = bids_layout.get(subject=subjid, modality='dwi', type='brainmask',
                           return_type='file', extensions=['nii', 'nii.gz'])

    # Freesurfer parcellation (from fmriprep)
    parc = bids_layout.get(subject=subjid, type='aseg',
                           return_type='file', extensions=['mgz'])

    if not parc:
        return nifti[0], (bvec[0], bval[0]), mask[0], None
    else:
        return nifti[0], (bvec[0], bval[0]), mask[0], parc[0]


def getBIDS(layout, wdir=None, nthreads=1):
    from nipype.pipeline import engine as pe
    from nipype.interfaces import utility as niu

    from mrtpipelines.interfaces import io

    BIDSDataGrabber = pe.Node(niu.Function(function=io._getData,
                                           input_names=['bids_layout',
                                                        'subjid'],
                                           output_names=['nifti',
                                                         'bdata',
                                                         'mask',
                                                         'parc']),
                                           name='BIDSDataGrabber')
    BIDSDataGrabber.base_dir = wdir
    BIDSDataGrabber.inputs.bids_layout = layout
    BIDSDataGrabber.interface.num_threads = nthreads

    return BIDSDataGrabber


def renameFile(file_name, node_name, wdir=None, nthreads=1):
    from nipype.pipeline import engine as pe
    from nipype.interfaces import utility as niu

    if nthreads >= 8:
        nthreads = np.int(nthreads / 4)

    renameFile = pe.Node(niu.Rename(format_string="%(subjid)s_%(file_name)s"),
                                    name=node_name)
    renameFile.base_dir = wdir
    renameFile.inputs.keep_ext = True
    renameFile.inputs.file_name = file_name
    renameFile.interface.num_threads = nthreads

    return renameFile


def subjSink(out_dir, wdir=None, nthreads=1):
    from nipype.pipeline import engine as pe
    from nipype.interfaces import io as nio

    if nthreads >= 8:
        nthreads = np.int(nthreads / 4)

    subjSink = pe.Node(nio.DataSink(), parameterization=False,
                                       name='subjSink')
    subjSink.base_dir = wdir
    subjSink.inputs.base_directory = out_dir
    subjSink.interface.num_threads = nthreads

    return subjSink
