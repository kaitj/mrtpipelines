from nipype import IdentityInterface
from nipype.pipeline import engine as pe

def getSubj(subjFile, work_dir):
    # Retrieve individual subject ids & number of subjectss
    subjids = []
    noSubj = 0
    with open(subjFile) as f:
        for subj in f:
            # temp = subj.lstrip('sub-')
            temp = subj.rstrip('\n')
            temp = 'sub-' + temp
            subjids.append(temp)
            noSubj += 1

    Subjid = pe.Node(IdentityInterface(fields=['subjid']), name='SubjectID')
    Subjid.base_dir = work_dir
    Subjid.iterables = [('subjid', subjids)]

    return Subjid, noSubj


def getData(bids_layout, subjid):
    # Strip leading 'sub-'
    subjid = subjid.lstrip('sub-')

    # Diffusion
    dwi = bids_layout.get(subject=subjid, modality='dwi', space='T1w',
                            type='preproc', return_type='file',
                            extensions=['nii', 'nii.gz'])
    bval = bids_layout.get(subject=subjid, modality='dwi', space='T1w',
                           type='preproc', return_type='file',
                           extensions=['bval'])
    bvec = bids_layout.get(subject=subjid, modality='dwi', space='T1w',
                           type='preproc', return_type='file',
                           extensions=['bvec'])
    mask = bids_layout.get(subject=subjid, modality='dwi', space='T1w',
                           type='brainmask', return_type='file',
                           extensions=['nii', 'nii.gz'])

    # Anatomical
    t1w = bids_layout.get(subject=subjid, modality='anat', type='T1w',
                          return_type='file', extensions=['nii', 'nii.gz'])
    t2w = bids_layout.get(subject=subjid, modality='anat', space='T1w',
                          type='T2w', return_type='file',
                          extensions=['nii', 'nii.gz'])

    return dwi[0], (bvec[0], bval[0]), mask[0], t1w[0], t2w[0]


def getBIDS(layout, wdir=None):
    from nipype.pipeline import engine as pe
    from nipype.interfaces import utility as niu

    from mrtpipelines.interfaces import io

    BIDSDataGrabber = pe.Node(niu.Function(function=io.getData,
                                           input_names=['bids_layout',
                                                        'subjid'],
                                           output_names=['dwi',
                                                         'bdata',
                                                         'mask',
                                                         't1w',
                                                         't2w']),
                                           name='BIDSDataGrabber')
    BIDSDataGrabber.base_dir = wdir
    BIDSDataGrabber.inputs.bids_layout = layout

    return BIDSDataGrabber


def copyFile(in_file, out_dir):
    import os, shutil, fnmatch

    # Check if output directory exists
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for curFile in in_file:
        if type(curFile) is list:
            curFile = curFile[-1]

        # Create new temp file with subjid label
        file_list = curFile.split('/')
        subjid = fnmatch.filter(file_list, '*subjid*')
        subjid = subjid[0].strip('_')

        out_file = subjid + '_' + file_list[-1]
        out_file = os.path.join(out_dir, out_file)

        shutil.copy2(curFile, out_file)

    return out_dir


def templateSink(out_dir, wdir=None):
    from nipype.pipeline import engine as pe
    from nipype.interfaces import io as nio

    tempSink = pe.Node(nio.DataSink(), parameterization=False,
                                       name='templateSink')
    tempSink.base_dir = wdir
    tempSink.inputs.base_directory = out_dir
    tempSink.inputs.container = 'template'

    return tempSink


def renameFile(file_name, node_name, wdir=None):
    from nipype.pipeline import engine as pe
    from nipype.interfaces import utility as niu

    renameFile = pe.MapNode(niu.Rename(format_string="%(subjid)s_%(file_name)s"),
                          iterfield=['in_file'], name=node_name)
    renameFile.base_dir = wdir
    renameFile.inputs.keep_ext = True
    renameFile.inputs.file_name = file_name

    return renameFile


def subjSink(out_dir, wdir=None):
    from nipype.pipeline import engine as pe
    from nipype.interfaces import io as nio

    subjSink = pe.Node(nio.DataSink(), parameterization=False,
                                       name='subjSink')
    subjSink.base_dir = wdir
    subjSink.inputs.base_directory = out_dir

    return subjSink
