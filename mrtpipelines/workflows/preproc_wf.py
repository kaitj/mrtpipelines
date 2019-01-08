from nipype.pipeline import engine as pe
from nipype.interfaces import utility as niu
from nipype.interfaces import mrtrix3 as mrt

from mrtpipelines.interfaces import io

# DEPRECATED
# def act_preproc_wf(shells=[0, 1000, 2000], lmax=[0, 8, 8], template_dir=None,
#                    template_label=None, wdir=None, nthreads=1,
#                    name='act_preproc_wf'):
#     """
#     Set up ACT response preproc workflow
#     Assumes files are registered to T1w space
#     """
#
#     if template_dir is None or template_label is None:
#         print("Missing template info")
#         raise IOError
#
#     # Grab template data
#     templateGrabber = io.getTemplate(template_dir=template_dir,
#                                      template_label=template_label,
#                                      wdir=wdir)
#
#     # Convert nii to mif
#     dwiConvert = pe.Node(mrt.MRConvert(), name='dwiConvert')
#     dwiConvert.base_dir = wdir
#     dwiConvert.inputs.nthreads = nthreads
#     dwiConvert.interface.num_threads = nthreads
#
#     # 5tt via freesurfer algorithm
#     gen5tt = pe.Node(mrt.Generate5tt(), name="gen5tt")
#     gen5tt.base_dir = wdir
#     gen5tt.inputs.algorithm = 'freesurfer'
#     gen5tt.inputs.args = '-nocrop'
#     gen5tt.inputs.out_file = 'space-T1w_5tt.mif'
#     gen5tt.inputs.nthreads = nthreads
#     gen5tt.interface.num_threads = nthreads
#
#     gen5ttMask = pe.Node(mrt.Generate5ttMask(), name='gen5ttMask')
#     gen5ttMask.base_dir = wdir
#     gen5ttMask.inputs.out_file = 'space-Template_5ttMask.mif'
#     gen5ttMask.inputs.nthreads = nthreads
#     gen5ttMask.interface.num_threads = nthreads
#
#     # dwi2response - included but no longer used
#     dwi2response = pe.Node(mrt.ResponseSD(), name='dwi2response')
#     dwi2response.base_dir = wdir
#     dwi2response.inputs.algorithm = 'msmt_5tt'
#     dwi2response.inputs.wm_file = 'space-T1w_wm.txt'
#     dwi2response.inputs.gm_file = 'space-T1w_gm.txt'
#     dwi2response.inputs.csf_file = 'space-dwi_csf.txt'
#     dwi2response.inputs.shell = shells
#     dwi2response.inputs.max_sh = lmax
#     dwi2response.inputs.nthreads = nthreads
#     dwi2response.interface.num_threads = nthreads
#
#     # Convert mask (nii) to mif
#     maskConvert = pe.Node(mrt.MRConvert(), name='maskConvert')
#     maskConvert.base_dir = wdir
#     maskConvert.inputs.nthreads = nthreads
#     maskConvert.interface.num_threads = nthreads
#
#     # dwi2fod
#     dwi2fod = pe.Node(mrt.EstimateFOD(), name='dwi2fod')
#     dwi2fod.base_dir = wdir
#     dwi2fod.inputs.algorithm = 'msmt_csd'
#     dwi2fod.inputs.shell = shells
#     dwi2fod.inputs.nthreads = nthreads
#     dwi2fod.interface.num_threads = nthreads
#
#     # mtnormalise
#     mtnormalise = pe.Node(mrt.MTNormalise(), name='mtnormalise')
#     mtnormalise.base_dir = wdir
#     mtnormalise.inputs.nthreads = nthreads
#     mtnormalise.interface.num_threads = nthreads
#
#     # Registration
#     MRRegister = pe.Node(mrt.MRRegister(), name='MRRegister')
#     MRRegister.base_dir = wdir
#     # MRRegister.inputs.ref_file = template
#     MRRegister.inputs.nl_warp = ['subj_2_template.mif',
#                                  'template_2_subj.mif']
#     MRRegister.inputs.nthreads = nthreads
#     MRRegister.interface.num_threads = nthreads
#
#     # Transforms
#     WarpSelect1 = pe.Node(niu.Select(), name='WarpSelect1')
#     WarpSelect1.base_dir = wdir
#     WarpSelect1.inputs.index = [0]
#     WarpSelect1.interface.num_threads = nthreads
#
#     WarpSelect2 = pe.Node(niu.Select(), name='WarpSelect2')
#     WarpSelect2.base_dir = wdir
#     WarpSelect2.inputs.index = [0]
#     WarpSelect2.interface.num_threads = nthreads
#
#     # Warp data
#     MaskTransform = pe.Node(mrt.MRTransform(), name='MaskTransform')
#     MaskTransform.base_dir = wdir
#     MaskTransform.inputs.out_file = 'space-Template_mask.mif'
#     MaskTransform.inputs.nthreads = nthreads
#     MaskTransform.interface.num_threads = nthreads
#
#     FODTransform = pe.Node(mrt.MRTransform(), name='FODTransform')
#     FODTransform.base_dir = wdir
#     FODTransform.inputs.out_file = 'space-Template_wmfod_norm.mif'
#     FODTransform.inputs.nthreads = nthreads
#     FODTransform.interface.num_threads = nthreads
#
#     ttTransform = pe.Node(mrt.MRTransform(), name='5ttTransform')
#     ttTransform.base_dir = wdir
#     ttTransform.inputs.out_file = 'space-Template_5tt.mif'
#     ttTransform.inputs.nthreads = nthreads
#     ttTransform.interface.num_threads = nthreads
#
#     # Tensor processing
#     DWINormalise = pe.Node(mrt.DWINormalise(), name='DWINormalise')
#     DWINormalise.base_dir = wdir
#     DWINormalise.inputs.out_file = 'space-T1w_norm.mif'
#     DWINormalise.inputs.nthreads = nthreads
#     DWINormalise.interface.num_threads = nthreads
#
#     DWITransform = pe.Node(mrt.MRTransform(), name='DWITransform')
#     DWITransform.base_dir = wdir
#     DWITransform.inputs.out_file = 'space-Template_norm.mif'
#     DWITransform.inputs.nthreads = nthreads
#     DWITransform.interface.num_threads = nthreads
#
#     FitTensor = pe.Node(mrt.FitTensor(), name='FitTensor')
#     FitTensor.base_dir = wdir
#     FitTensor.inputs.out_file = 'space-Template_tensor.mif'
#     FitTensor.inputs.nthreads = nthreads
#     FitTensor.interface.num_threads = nthreads
#
#     TensorMetrics = pe.Node(mrt.TensorMetrics(), name='TensorMetrics')
#     TensorMetrics.base_dir = wdir
#     TensorMetrics.inputs.out_fa = 'space-Template_fa.mif'
#     TensorMetrics.inputs.out_adc = 'space-Template_md.mif'
#     TensorMetrics.inputs.out_ad = 'space-Template_ad.mif'
#     TensorMetrics.inputs.out_rd = 'space-Template_rd.mif'
#     TensorMetrics.inputs.nthreads = nthreads
#     TensorMetrics.interface.num_threads = nthreads
#
#     # Build workflow
#     workflow = pe.Workflow(name=name)
#
#     workflow.connect([
#         # Compute FOD
#         (dwiConvert, dwi2response, [('out_file', 'in_file')]),
#         (gen5tt, dwi2response, [('out_file', 'mtt_file')]),
#         (maskConvert, dwi2response, [('out_file', 'in_file')]),
#         (dwiConvert, dwi2fod, [('out_file', 'in_file')]),
#         (templateGrabber, dwi2fod, [('wm_response', 'wm_txt'),
#                                     ('gm_response', 'gm_txt'),
#                                     ('csf_response', 'csf_txt')]),
#         (dwi2fod, mtnormalise, [('wm_odf', 'in_wm'),
#                                 ('gm_odf', 'in_gm'),
#                                 ('csf_odf', 'in_csf')]),
#         (maskConvert, mtnormalise, [('out_file', 'mask')]),
#         (templateGrabber, MRRegister, [('wm_fod', 'ref_file')]),
#         (mtnormalise, MRRegister, [('out_wm', 'in_file')]),
#         (MRRegister, WarpSelect1, [('nl_warp', 'inlist')]),
#         (MRRegister, WarpSelect2, [('nl_warp', 'inlist')]),
#         (maskConvert, MaskTransform, [('out_file', 'in_file')])
#         (WarpSelect1, MaskTransform, [('out', 'warp')]),
#         (mtnormalise, FODTransform, [('out_wm', 'in_file')]),
#         (WarpSelect1, FODTransform, [('out', 'warp')]),
#         (gen5tt, ttTransform, [('out_file', 'in_file')]),
#         (WarpSelect1, ttTransform, [('out', 'warp')])
#         (ttTransform, gen5ttMask, [('out_file', 'in_file')])
#         # Compute tensors
#         (dwiConvert, DWINormalise, [('out_file', 'in_file')]),
#         (maskConvert, DWINormalise, [('out_file', 'in_mask')]),
#         (DWINormalise, DWITransform, [('out_file', 'in_file')]),
#         (WarpSelect1, DWITransform, [('out', 'warp')]),
#         (DWITransform, FitTensor, [('out_file', 'in_file')]),
#         (MaskTransform, FitTensor, [('out_file', 'in_mask')]),
#         (FitTensor, TensorMetrics, [('out_file', 'in_file')]),
#         (MaskTransform, TensorMetrics, [('out_file', 'in_mask')])
#     ])
#
#     return workflow


def dholl_preproc_wf(shells=[0, 1000, 2000], lmax=[0, 8, 8], sshell=False,
                     template_dir=None, template_label=None,
                     wdir=None, nthreads=1, name='dholl_preproc_wf'):
    """
    Set up Dhollander response preproc workflow
    No assumption of registration to T1w space is made
    """

    if template_dir is None or template_label is None:
        print("Missing template info")
        raise IOError

    # Grab template data
    templateGrabber = io.getTemplate(template_dir=template_dir,
                                     template_label=template_label,
                                     wdir=wdir)

    # Convert nii to mif
    dwiConvert = pe.Node(mrt.MRConvert(), name='dwiConvert')
    dwiConvert.base_dir = wdir
    dwiConvert.inputs.nthreads = nthreads
    dwiConvert.interface.num_threads = nthreads

    # dwi2response - included but not used
    dwi2response = pe.Node(mrt.ResponseSD(), name='dwi2response')
    dwi2response.base_dir = wdir
    dwi2response.inputs.algorithm = 'dhollander'
    dwi2response.inputs.wm_file = 'space-dwi_wm.txt'
    dwi2response.inputs.gm_file = 'space-dwi_gm.txt'
    dwi2response.inputs.csf_file = 'space-dwi_csf.txt'
    dwi2response.inputs.max_sh = lmax
    dwi2response.inputs.shell = shells
    dwi2response.inputs.nthreads = nthreads
    dwi2response.interface.num_threads = nthreads

    # Convert mask (nii) to mif
    maskConvert = pe.Node(mrt.MRConvert(), name='maskConvert')
    maskConvert.base_dir = wdir
    maskConvert.inputs.nthreads = nthreads
    maskConvert.interface.num_threads = nthreads

    # dwi2fod
    dwi2fod = pe.Node(mrt.EstimateFOD(), name='dwi2fod')
    dwi2fod.base_dir = wdir
    dwi2fod.inputs.algorithm = 'msmt_csd'
    dwi2fod.inputs.shell = shells
    dwi2fod.inputs.nthreads = nthreads
    dwi2fod.interface.num_threads = nthreads

    # mtnormalise
    mtnormalise = pe.Node(mrt.MTNormalise(), name='mtnormalise')
    mtnormalise.base_dir = wdir
    mtnormalise.inputs.nthreads = nthreads
    mtnormalise.interface.num_threads = nthreads

    # Registration
    MRRegister = pe.Node(mrt.MRRegister(), name='MRRegister')
    MRRegister.base_dir = wdir
    # MRRegister.inputs.ref_file = template
    MRRegister.inputs.nl_warp = ['subj_2_template.mif',
                                 'template_2_subj.mif']
    MRRegister.inputs.nthreads = nthreads
    MRRegister.interface.num_threads = nthreads

    # Transforms
    WarpSelect1 = pe.Node(niu.Select(), name='WarpSelect1')
    WarpSelect1.base_dir = wdir
    WarpSelect1.inputs.index = [0]
    WarpSelect1.interface.num_threads = nthreads

    WarpSelect2 = pe.Node(niu.Select(), name='WarpSelect2')
    WarpSelect2.base_dir = wdir
    WarpSelect2.inputs.index = [1]
    WarpSelect2.interface.num_threads = nthreads

    # Warp data
    MaskTransform = pe.Node(mrt.MRTransform(), name='MaskTransform')
    MaskTransform.base_dir = wdir
    MaskTransform.inputs.out_file = 'space-Template_mask.mif'
    MaskTransform.inputs.nthreads = nthreads
    MaskTransform.interface.num_threads = nthreads

    FODTransform = pe.Node(mrt.MRTransform(), name='FODTransform')
    FODTransform.base_dir = wdir
    FODTransform.inputs.out_file = 'space-Template_wmfod_norm.mif'
    FODTransform.inputs.nthreads = nthreads
    FODTransform.interface.num_threads = nthreads

    # Tensor processing
    DWINormalise = pe.Node(mrt.DWINormalise(), name='DWINormalise')
    DWINormalise.base_dir = wdir
    DWINormalise.inputs.out_file = 'space-dwi_norm.mif'
    DWINormalise.inputs.nthreads = nthreads
    DWINormalise.interface.num_threads = nthreads

    DWITransform = pe.Node(mrt.MRTransform(), name='DWITransform')
    DWITransform.base_dir = wdir
    DWITransform.inputs.out_file = 'space-Template_norm.mif'
    DWITransform.inputs.nthreads = nthreads
    DWITransform.interface.num_threads = nthreads

    FitTensor = pe.Node(mrt.FitTensor(), name='FitTensor')
    FitTensor.base_dir = wdir
    FitTensor.inputs.out_file = 'space-Template_tensor.mif'
    FitTensor.inputs.nthreads = nthreads
    FitTensor.interface.num_threads = nthreads

    TensorMetrics = pe.Node(mrt.TensorMetrics(), name='TensorMetrics')
    TensorMetrics.base_dir = wdir
    TensorMetrics.inputs.out_fa = 'space-Template_fa.mif'
    TensorMetrics.inputs.out_adc = 'space-Template_md.mif'
    TensorMetrics.inputs.out_ad = 'space-Template_ad.mif'
    TensorMetrics.inputs.out_rd = 'space-Template_rd.mif'
    TensorMetrics.inputs.nthreads = nthreads
    TensorMetrics.interface.num_threads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    # Single shell
    if sshell is True:
        workflow.connect([
            # Compute FOD
            (dwiConvert, dwi2response, [('out_file', 'in_file')]),
            (dwiConvert, dwi2fod, [('out_file', 'in_file')]),
            (dwi2response, dwi2fod, [('wm_file', 'wm_txt'),
                                    ('csf_file', 'csf_txt')]),
            (dwi2fod, mtnormalise, [('wm_odf', 'in_wm'),
                                    ('csf_odf', 'in_csf')]),
            (maskConvert, mtnormalise, [('out_file', 'mask')]),
            (maskConvert, MRRegister, [('out_file', 'mask1')]),
            (templateGrabber, MRRegister, [('wm_fod', 'ref_file'),
                                           ('mask', 'mask2')]),
            (mtnormalise, MRRegister, [('out_wm', 'in_file')]),
            (MRRegister, WarpSelect1, [('nl_warp', 'inlist')]),
            (MRRegister, WarpSelect2, [('nl_warp', 'inlist')]),
            (maskConvert, MaskTransform, [('out_file', 'in_file')]),
            (WarpSelect1, MaskTransform, [('out', 'warp')]),
            (mtnormalise, FODTransform, [('out_wm', 'in_file')]),
            (WarpSelect1, FODTransform, [('out', 'warp')]),
            # Compute tensors
            (dwiConvert, DWINormalise, [('out_file', 'in_file')]),
            (maskConvert, DWINormalise, [('out_file', 'in_mask')]),
            (DWINormalise, DWITransform, [('out_file', 'in_file')]),
            (WarpSelect1, DWITransform, [('out', 'warp')]),
            (DWITransform, FitTensor, [('out_file', 'in_file')]),
            (MaskTransform, FitTensor, [('out_file', 'in_mask')]),
            (FitTensor, TensorMetrics, [('out_file', 'in_file')]),
            (MaskTransform, TensorMetrics, [('out_file', 'in_mask')])
        ])

    # For multi-shell
    else:
        workflow.connect([
            # Compute FOD
            (dwiConvert, dwi2response, [('out_file', 'in_file')]),
            (dwiConvert, dwi2fod, [('out_file', 'in_file')]),
            (dwi2response, dwi2fod, [('wm_file', 'wm_txt'),
                                     ('gm_file', 'gm_txt'),
                                     ('csf_file', 'csf_txt')]),
            (dwi2fod, mtnormalise, [('wm_odf', 'in_wm'),
                                    ('gm_odf', 'in_gm'),
                                    ('csf_odf', 'in_csf')]),
            (maskConvert, mtnormalise, [('out_file', 'mask')]),
            (maskConvert, MRRegister, [('out_file', 'mask1')]),
            (templateGrabber, MRRegister, [('wm_fod', 'ref_file'),
                                           ('mask', 'mask2')]),
            (mtnormalise, MRRegister, [('out_wm', 'in_file')]),
            (MRRegister, WarpSelect1, [('nl_warp', 'inlist')]),
            (MRRegister, WarpSelect2, [('nl_warp', 'inlist')]),
            (maskConvert, MaskTransform, [('out_file', 'in_file')]),
            (WarpSelect1, MaskTransform, [('out', 'warp')]),
            (mtnormalise, FODTransform, [('out_wm', 'in_file')]),
            (WarpSelect1, FODTransform, [('out', 'warp')]),
            # Compute tensors
            (dwiConvert, DWINormalise, [('out_file', 'in_file')]),
            (maskConvert, DWINormalise, [('out_file', 'in_mask')]),
            (DWINormalise, DWITransform, [('out_file', 'in_file')]),
            (WarpSelect1, DWITransform, [('out', 'warp')]),
            (DWITransform, FitTensor, [('out_file', 'in_file')]),
            (MaskTransform, FitTensor, [('out_file', 'in_mask')]),
            (FitTensor, TensorMetrics, [('out_file', 'in_file')]),
            (MaskTransform, TensorMetrics, [('out_file', 'in_mask')])
        ])

    return workflow
