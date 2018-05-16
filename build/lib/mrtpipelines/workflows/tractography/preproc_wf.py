from nipype.pipeline import engine as pe
from nipype.interfaces import utility as niu
from nipype.interfaces import mrtrix3 as mrt

from ...interfaces import DataGrabber as dg

def act_preproc_wf(bids_dir, subjid, wdir=None, nthreads=1, name='act_preproc_wf'):
    """
    Set up ACT preproc workflow
    """
    # Instantiate Nodes
    # Convert from nii to mif
    MRConvert = pe.Node(mrt.MRConvert(), name="MRConvert")
    MRConvert.base_dir = wdir
    MRConvert.inputs.nthreads = nthreads

    # Generate 5 tissue-type using free surfer algorithm [T1w-space]
    Gen5tt = pe.Node(mrt.Generate5tt(), name="Generate5tt")
    Gen5tt.inputs.algorithm = 'freesurfer'
    Gen5tt.inputs.args = '-nocrop'
    Gen5tt.inputs.out_file = '5tt.mif'
    Gen5tt.inputs.nthreads = nthreads

    # dwi2response
    dwi2response = pe.Node(mrt.ResponseSD(), name='dwi2response')
    dwi2response.inputs.algorithm = 'msmt_5tt'
    dwi2response.inputs.wm_file = 'wm.txt'
    dwi2response.inputs.gm_file = 'gm.txt'
    dwi2response.inputs.csf_file = 'csf.txt'
    dwi2response.inputs.nthreads = nthreads

    # dwi2mask
    dwi2mask = pe.Node(mrt.BrainMask(), name='dwi2mask')
    dwi2mask.inputs.out_file = 'dwi_mask.mif'
    dwi2mask.inputs.nthreads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (BIDSDataGrabber, MRConvert, [("nifti", "in_file"),
                                                            ("bdata", "grad_fsl")]),
        (BIDSDataGrabber, Gen5tt, [('parc', 'in_file')]),
        (BIDSDataGrabber, dwi2response, [('bdata', 'grad_fsl')]),
        (MRConvert, dwi2response, [('out_file', 'in_file')]),
        (Gen5tt, dwi2response, [('out_file', 'in_file')]),
        (BIDSDataGrabber, dwi2mask, [('bdata', 'grad_fsl')]),
        (MRConvert, dwi2mask, [('out_file', 'in_file')])])

    return workflow
