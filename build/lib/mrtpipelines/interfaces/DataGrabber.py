def getExecOpt(bids_dir, subjid, wdir, nthreads):
    return bids_dir, subjid, wdir, nthreads

def getData(bids_dir, subjid, wdir):
    from bids.grabbids import BIDSLayout

    layout = BIDSLayout(bids_dir)

    # Diffusion
    nifti = layout.get(subject=subjid, modality='dwi', space='T1w', type='preproc',
                                return_type='file', extensions=['nii', 'nii.gz'])
    bval = layout.get(subject=subjid, modality='dwi', space='T1w', type='preproc',
                                return_type='file', extensions=['bval'])
    bvec = layout.get(subject=subjid, modality='dwi', space='T1w', type='preproc',
                                return_type='file', extensions=['bvec'])

    # Freesurfer parcellation (from fmriprep)
    parc = layout.get(subject=subjid, type='aseg', return_type='file', extensions=['mgz'])

    return nifti[0], (bvec[0], bval[0]), parc[0]
