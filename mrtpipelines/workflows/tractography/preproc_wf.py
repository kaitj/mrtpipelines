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
    Generate5tt.inputs.out_file = 'space-T1w_5tt.mif'
    Generate5tt.inputs.nthreads = nthreads

    # dwi2response
    dwi2response = pe.Node(mrt.ResponseSD(), name='dwi2response')
    dwi2response.inputs.algorithm = 'msmt_5tt'
    dwi2response.inputs.wm_file = 'space-T1w_wm.txt'
    dwi2response.inputs.gm_file = 'space-T1w_gm.txt'
    dwi2response.inputs.csf_file = 'space-T1w_csf.txt'
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
    MRRegister.inputs.nl_warp = ['mov_sub-tmp_warp.mif', 'sub-tmp_mov_warp.mif']
    MRRegister.inputs.nthreads = nthreads

    # Transform subjects' data into template space
    WarpSelect1 = pe.MapNode(niu.Select(), iterfield=['inlist'],
                                           name='WarpSelect1')
    WarpSelect1.base_dir = wdir
    WarpSelect1.inputs.index = [0]

    WarpSelect2 = pe.MapNode(niu.Select(), iterfield=['inlist'],
                                           name='WarpSelect2')
    WarpSelect2.base_dir = wdir
    WarpSelect2.inputs.index = [1]

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
    gen5ttMask.inputs.out_file = 'space-Template_5ttMask.mif'
    gen5ttMask.inputs.nthreads = nthreads

    # Generate tractography
    genTract = pe.MapNode(mrt.Tractography(), iterfield=['in_file',
                                                         'act_file',
                                                         'seed_gmwmi'],
                                              name='genTract')
    genTract.base_dir = wdir
    genTract.inputs.backtrack
    genTract.inputs.n_tracks = 200000
    genTract.inputs.out_file = 'space-Template_variant-tckgen_streamlines-200K_tract.tck'
    genTract.inputs.nthreads = nthreads

    # Sphereical-deconvoulution informed filtering of tractography
    siftTract = pe.MapNode(mrt.SIFT(), iterfield=['in_file', 'in_fod'],
                                       name='tcksift')
    siftTract.base_dir = wdir
    siftTract.inputs.term_number = 100000
    siftTract.inputs.out_file = 'space-Template_variant-sift_streamlines-100K_tract.tck'
    siftTract.inputs.nthreads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (MRRegister, WarpSelect1, [('nl_warp', 'inlist')]),
        (MRRegister, WarpSelect2, [('nl_warp', 'inlist')]),
        (WarpSelect1, FODTransform, [('out', 'warp')]),
        (WarpSelect1, AnatTransform, [('out', 'warp')]),
        (AnatTransform, gen5ttMask, [('out_file', 'in_file')]),
        (AnatTransform, genTract, [('out_file', 'act_file')]),
        (gen5ttMask, genTract, [('out_file', 'seed_gmwmi')]),
        (FODTransform, genTract, [('out_file', 'in_file')]),
        (genTract, siftTract, [('out_file', 'in_file')]),
        (FODTransform, siftTract, [('out_file', 'in_fod')])
    ])

    return workflow
