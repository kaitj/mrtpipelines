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
    nifti = bids_layout.get(subject=subjid, modality='dwi', space='T1w', type='preproc',
                                return_type='file', extensions=['nii', 'nii.gz'])
    bval = bids_layout.get(subject=subjid, modality='dwi', space='T1w', type='preproc',
                                return_type='file', extensions=['bval'])
    bvec = bids_layout.get(subject=subjid, modality='dwi', space='T1w', type='preproc',
                                return_type='file', extensions=['bvec'])

    # Freesurfer parcellation (from fmriprep)
    parc = bids_layout.get(subject=subjid, type='aseg', return_type='file', extensions=['mgz'])

    return nifti[0], (bvec[0], bval[0]), parc[0]
