from nipype import IdentityInterface
from nipype.pipeline import engine as pe

import numpy as np

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


def getData(bids_layout, subjid):
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

    BIDSDataGrabber = pe.Node(niu.Function(function=io.getData,
                                           input_names=['bids_layout',
                                                        'subjid'],
                                           output_names=['nifti',
                                                         'bdata',
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
