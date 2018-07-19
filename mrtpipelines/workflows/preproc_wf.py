from nipype.pipeline import engine as pe
from nipype.interfaces import utility as niu
from nipype.interfaces import mrtrix3 as mrt

def hcp_preproc_wf(wdir=None, nthreads=1, name='hcp_preproc_wf'):
    """
    Set up dhollander response preproc workflow
    """

    if nthreads >= 8:
        nthreads = 8

    # Convert from nii to mif
    dataConvert = pe.Node(mrt.MRConvert(), name="dataConvert")
    dataConvert.base_dir = wdir
    dataConvert.inputs.nthreads = nthreads

    # dwi2response
    dwi2response = pe.Node(mrt.ResponseSD(), name='dwi2response')
    dwi2response.base_dir = wdir
    dwi2response.inputs.algorithm = 'dhollander'
    dwi2response.inputs.wm_file = 'space-dwi_wm.txt'
    dwi2response.inputs.gm_file = 'space-dwi_gm.txt'
    dwi2response.inputs.csf_file = 'space-dwi_csf.txt'
    dwi2response.inputs.max_sh = [0, 8, 8, 8]
    dwi2response.inputs.nthreads = nthreads

    # dwi2mask
    maskConvert = pe.Node(mrt.MRConvert(), name='maskConvert')
    maskConvert.base_dir = wdir
    maskConvert.inputs.nthreads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.add_nodes([maskConvert])
    workflow.connect([
        (dataConvert, dwi2response, [('out_file', 'in_file')])
    ])

    return workflow


def prepTensor_wf(wdir=None, nthreads=1, name='prepTensor_wf'):
    """
    Set up workflow to generate Tractography
    """

    if nthreads >= 8:
        nthreads = 8

    # Register subjects to template
    MRRegister = pe.MapNode(mrt.MRRegister(), iterfield=['in_file', 'mask1'],
                                              name='MRRegister')
    MRRegister.base_wdir = wdir
    MRRegister.inputs.nl_warp = ['subj2template_warp.mif',
                                 'template2subj_warp.mif']
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

    MaskTransform = pe.MapNode(mrt.MRTransform(), iterfield=['in_file', 'warp'],
                                                  name='MaskTransform')
    MaskTransform.base_dir = wdir
    MaskTransform.inputs.out_file = 'space-Template_mask.mif'
    MaskTransform.inputs.nthreads = nthreads

    MaskSelect = pe.MapNode(niu.Select(), iterfield=['inlist'],
                                          name='MaskSelect')
    MaskSelect.base_dir = wdir
    MaskSelect.inputs.index = [0]

    DWINormalise = pe.MapNode(mrt.DWINormalise(), iterfield=['in_file'],
                                                  name='DWINormalise')
    DWINormalise.base_dir = wdir
    DWINormalise.inputs.out_file = 'space-T1w_norm.mif'
    DWINormalise.inputs.nthreads = nthreads

    DWITransform = pe.MapNode(mrt.MRTransform(), iterfield=['in_file', 'warp'],
                                                  name='DWITransform')
    DWITransform.base_dir = wdir
    DWITransform.inputs.out_file = 'space-Template_norm.mif'
    DWITransform.inputs.nthreads = nthreads

    FitTensor = pe.MapNode(mrt.FitTensor(), iterfield=['in_file', 'in_mask'],
                                            name='FitTensor')
    FitTensor.base_dir = wdir
    FitTensor.inputs.out_file = 'space-Template_tensor.mif'
    FitTensor.inputs.nthreads = nthreads

    TensorMetrics = pe.MapNode(mrt.TensorMetrics(), iterfield=['in_file',
                                                               'in_mask'],
                                                    name='TensorMetrics')
    TensorMetrics.base_dir = wdir
    TensorMetrics.inputs.out_fa = 'space-Template_fa.mif'
    TensorMetrics.inputs.out_adc = 'space-Template_md.mif'
    TensorMetrics.inputs.out_ad = 'space-Template_ad.mif'
    TensorMetrics.inputs.out_rd = 'space-Template_rd.mif'
    TensorMetrics.inputs.nthreads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (MRRegister, WarpSelect1, [('nl_warp', 'inlist')]),
        (MRRegister, WarpSelect2, [('nl_warp', 'inlist')]),
        (WarpSelect1, MaskTransform, [('out', 'warp')]),
        (DWINormalise, DWITransform, [('out_file', 'in_file')]),
        (WarpSelect1, DWITransform, [('out', 'warp')]),
        (DWITransform, FitTensor, [('out_file', 'in_file')]),
        (MaskTransform, FitTensor, [('out_file', 'in_mask')]),
        (FitTensor, TensorMetrics, [('out_file', 'in_file')]),
        (MaskTransform, TensorMetrics, [('out_file', 'in_mask')]),
        (MaskTransform, MaskSelect, [('out_file', 'inlist')])
    ])

    return workflow
