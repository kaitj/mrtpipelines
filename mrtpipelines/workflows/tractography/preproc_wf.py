from nipype.pipeline import engine as pe
from nipype.interfaces import utility as niu
from nipype.interfaces import mrtrix3 as mrt

def act_preproc_wf(wdir=None, nthreads=4, name='act_preproc_wf'):
    """
    Set up ACT preproc workflow
    """

    # Define each node to use 4 cores if available
    if nthreads >= 4:
        nthreads = 4

    # Convert from nii to mif
    MRConvert = pe.Node(mrt.MRConvert(), name="MRConvert")
    MRConvert.base_dir = wdir
    MRConvert.inputs.nthreads = nthreads

    # Generate 5 tissue-type using free surfer algorithm [T1w-space]
    Generate5tt = pe.Node(mrt.Generate5tt(), name="Generate5tt")
    Generate5tt.inputs.algorithm = 'freesurfer'
    Generate5tt.inputs.args = '-nocrop'
    Generate5tt.inputs.out_file = '5tt.mif'
    Generate5tt.inputs.nthreads = nthreads

    # dwi2response
    dwi2response = pe.Node(mrt.ResponseSD(), name='dwi2response')
    dwi2response.inputs.algorithm = 'msmt_5tt'
    dwi2response.inputs.wm_file = 'wm.txt'
    dwi2response.inputs.gm_file = 'gm.txt'
    dwi2response.inputs.csf_file = 'csf.txt'
    dwi2response.inputs.max_sh = [0, 8, 8]
    dwi2response.inputs.nthreads = nthreads

    # dwi2mask
    dwi2mask = pe.Node(mrt.BrainMask(), name='dwi2mask')
    dwi2mask.inputs.out_file = 'dwi_mask.mif'
    dwi2mask.inputs.nthreads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (MRConvert, dwi2response, [('out_file', 'in_file')]),
        (Generate5tt, dwi2response, [('out_file', 'mtt_file')]),
        (MRConvert, dwi2mask, [('out_file', 'in_file')])
    ])

    return workflow

def prepACTTract_wf(wdir=None, nthreads=1, name='prepACTTract_wf'):
    """
    Set up workflow to generate Tractography
    """

    # Define nodes to use 4 cores if available
    if nthreads >= 4:
        nthreads = 4

    # Register subjects to template
    MRRegister = pe.MapNode(mrt.MRRegister(), iterfield=['in_file', 'mask1'],
                                              name='MRRegister')
    MRRegister.base_wdir = wdir
    MRRegister.inputs.nl_warp = ['mov-tmp_warp.mif', 'tmp-mov_warp.mif']
    MRRegister.inputs.nthreads = nthreads

    # Transform subjects' data into template space
    WarpSelect = pe.MapNode(niu.Select(), iterfield=['inlist'],
                                          name='WarpSelect')
    WarpSelect.base_dir = wdir
    WarpSelect.inputs.index = [0]

    FODTransform = pe.MapNode(mrt.MRTransform(), iterfield=['in_file', 'warp'],
                                                 name='FODTransform')
    FODTransform.base_dir = wdir
    FODTransform.inputs.out_file = 'space-Template_wmfod.mif'
    FODTransform.inputs.nthreads = nthreads

    AnatTransform = pe.MapNode(mrt.MRTransform(), iterfield=['in_file', 'warp'],
                                                  name='AnatTransform')
    AnatTransform.base_dir = wdir
    AnatTransform.inputs.out_file = 'space-Template_5tt.mif'
    AnatTransform.inputs.nthreads = nthreads

    # Generate 5tt mask
    gen5ttMask = pe.MapNode(mrt.Generate5ttMask(), iterfield=['in_file'],
                                                   name='gen5ttMask')
    gen5ttMask.base_dir = wdir
    gen5ttMask.inputs.nthreads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (MRRegister, WarpSelect, [('nl_warp', 'inlist')]),
        (WarpSelect, FODTransform, [('out', 'warp')]),
        (WarpSelect, AnatTransform, [('out', 'warp')]),
        (AnatTransform, gen5ttMask, [('out_file', 'in_file')])
    ])

    return workflow
