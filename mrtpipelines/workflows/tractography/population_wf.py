from nipype.pipeline import engine as pe
from nipype.interfaces import mrtrix3 as mrt

def pop_template_wf(wdir=None, nthreads=1, name='population_template_wf'):

    # Estimate group response for each tissue type
    avg_wm = pe.JoinNode(mrt.AverageResponse(), joinsource='SubjectID',
                                                joinfield=['in_files'],
                                                name='avgResponse_wm')
    avg_wm.base_dir = wdir
    avg_wm.inputs.out_file = 'avg_wm.txt'

    avg_gm = pe.JoinNode(mrt.AverageResponse(), joinsource='SubjectID',
                                                joinfield=['in_files'],
                                                name='avgResponse_gm')
    avg_gm.base_dir = wdir
    avg_gm.inputs.out_file = 'avg_gm.txt'

    avg_csf = pe.JoinNode(mrt.AverageResponse(), joinsource='SubjectID',
                                                 joinfield=['in_files'],
                                                 name='avgResponse_csf')
    avg_csf.base_dir = wdir
    avg_csf.inputs.out_file = 'avg_csf.txt'

    # dwi2fod
    dwi2fod = pe.MapNode(mrt.EstimateFOD(), name-'dwi2fod')
    dwi2fod.inputs.algorithm = 'msmt_csd'

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (avg_wm, dwi2fod, [('out_file'), 'wm_txt']),
        (avg_gm, dwi2fod, [('out_file'), 'gm_txt']),
        (avg_csf, dwi2fod, [('out_file'), 'csf_txt'])
    ])

    return workflow
