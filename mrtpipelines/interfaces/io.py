from nipype import IdentityInterface
from nipype.pipeline import engine as pe

def getSubj(subjFile, work_dir):
    # Retrieve individual subject ids
    subjids = []
    with open(subjFile) as f:
        for subj in f:
            temp = subj.lstrip('sub-')
            temp = temp.rstrip('\n')
            subjids.append(temp)

    Subjid = pe.Node(IdentityInterface(fields=['subjid']), name='SubjectID')
    Subjid.base_dir = work_dir
    Subjid.iterables = [('subjid', subjids)]

    return Subjid


def getData(bids_layout, subjid):
    # Diffusion
    nifti = bids_layout.get(subject=subjid, modality='dwi', space='T1w',
                            type='preproc', return_type='file',
                            extensions=['nii', 'nii.gz'])
    bval = bids_layout.get(subject=subjid, modality='dwi', space='T1w',
                           type='preproc', return_type='file',
                           extensions=['bval'])
    bvec = bids_layout.get(subject=subjid, modality='dwi', space='T1w',
                           type='preproc', return_type='file',
                           extensions=['bvec'])

    # Freesurfer parcellation (from fmriprep)
    parc = bids_layout.get(subject=subjid, type='aseg', return_type='file',
                           extensions=['mgz'])

    return nifti[0], (bvec[0], bval[0]), parc[0]


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
