from nipype.pipeline import engine as pe
from nipype.interfaces import utility as niu
from nipype.interfaces import io as nio

def _getTemplate(template_dir, template_label, work_dir):
    import os.path as op

    resdir = op.realpath(op.join(template_dir, 'response'))
    dwidir = op.realpath(op.join(template_dir, 'dwi'))

    wm_fod = template_label + '_wmfod.mif'
    wm_fod = op.join(resdir, wm_fod)
    wm_response = template_label + '_wmresponse.txt'
    wm_response = op.join(resdir, wm_response)
    gm_response = template_label + '_gmresponse.txt'
    gm_response = op.join(resdir, gm_response)
    csf_response = template_label + '_csfresponse.txt'
    csf_response = op.join(resdir, csf_response)
    mask = template_label + '_brainmask.mif'
    mask = op.join(dwidir, mask)

    return wm_fod, wm_response, gm_response, csf_response, mask

def getTemplate(template_dir, template_label, wdir=None):
    getTemplate = pe.Node(niu.Function(function=_getTemplate,
                                        input_names=['template_dir',
                                                     'template_label',
                                                     'work_dir'],
                                        output_names=['wm_fod',
                                                      'wm_response',
                                                      'gm_response',
                                                      'csf_response',
                                                      'mask']),
                                        name='getTemplate')

    getTemplate.base_dir = wdir
    getTemplate.inputs.template_dir = template_dir
    getTemplate.inputs.template_label = template_label
    getTemplate.inputs.work_dir = wdir

    return getTemplate


def _getData(bids_layout, subjid, bmask):
    # Strip leading 'sub-'
    subj = subjid.lstrip('sub-')

    # Diffusion
    nifti = bids_layout.get(subject=subj, modality='dwi', type='preproc',
                            return_type='file', extensions=['nii', 'nii.gz'])
    bval = bids_layout.get(subject=subj, modality='dwi', type='preproc',
                           return_type='file', extensions=['bval'])
    bvec = bids_layout.get(subject=subj, modality='dwi', type='preproc',
                           return_type='file', extensions=['bvec'])

    if bmask is None:
        mask = bids_layout.get(subject=subj, modality='dwi', type='brainmask',
                               return_type='file', extensions=['nii', 'nii.gz'])

        return subjid, nifti[0], (bvec[0], bval[0]), mask[0]
    else:
        mask = bmask

        return subjid, nifti[0], (bvec[0], bval[0]), mask


def getBIDS(layout, subj, bmask, wdir=None, nthreads=1):
    BIDSDataGrabber = pe.Node(niu.Function(function=_getData,
                                           input_names=['bids_layout',
                                                        'subjid',
                                                        'bmask'],
                                           output_names=['subjid',
                                                         'nifti',
                                                         'bdata',
                                                         'mask']),
                                           name='BIDSDataGrabber')
    BIDSDataGrabber.base_dir = wdir
    BIDSDataGrabber.inputs.bids_layout = layout
    BIDSDataGrabber.inputs.subjid = subj
    BIDSDataGrabber.inputs.bmask = bmask
    BIDSDataGrabber.interface.num_threads = nthreads

    return BIDSDataGrabber


def _getScalarData(bids_layout, subjid, scalar):
    # Strip leading 'sub-'
    subj = subjid.lstrip('sub-')

    # Diffusion
    tract = bids_layout.get(subject=subj, type='tractography',
                            return_type='file', extensions=['tck'])
    scalar = bids_layout.get(subject=subj, type=scalar,
                             return_type='file', extensions=['nii', 'nii.gz', 'mif'])

    return subjid, tract[0], scalar[0]


def getScalarData(layout, subj, scalar, wdir=None, nthreads=1):
    BIDSScalarGrabber = pe.Node(niu.Function(function=_getScalarData,
                                           input_names=['bids_layout',
                                                        'subjid',
                                                        'scalar'],
                                           output_names=['subjid',
                                                         'tract',
                                                         'scalar']),
                                           name='BIDSScalarGrabber')
    BIDSScalarGrabber.base_dir = wdir
    BIDSScalarGrabber.inputs.bids_layout = layout
    BIDSScalarGrabber.inputs.subjid = subj
    BIDSScalarGrabber.inputs.scalar = scalar
    BIDSScalarGrabber.interface.num_threads = nthreads

    return BIDSScalarGrabber


def renameFile(file_name, node_name, wdir=None, nthreads=1):
    renameFile = pe.Node(niu.Rename(format_string="%(subjid)s_%(file_name)s"),
                                    name=node_name)
    renameFile.base_dir = wdir
    renameFile.inputs.keep_ext = True
    renameFile.inputs.file_name = file_name
    renameFile.interface.num_threads = nthreads

    return renameFile


def subjSink(out_dir, wdir=None, nthreads=1):
    subjSink = pe.Node(nio.DataSink(), parameterization=False,
                                       name='subjSink')
    subjSink.base_dir = wdir
    subjSink.inputs.base_directory = out_dir
    subjSink.interface.num_threads = nthreads

    return subjSink
