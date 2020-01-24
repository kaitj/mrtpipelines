from nipype.pipeline import engine as pe
from nipype.interfaces import mrtrix3 as mrt
from nipype.interfaces import utility as niu

def tckSample(wdir=None, nthreads=1):
    tckSample = pe.Node(mrt.TCKSample(), name='tckSample')
    tckSample.base_dir = wdir
    tckSample.inputs.out_file = "scalar.txt"
    tckSample.inputs.nthreads = nthreads
    tckSample.interface.num_threads = nthreads

    return tckSample

def _writeScalar(in_file, wdir):
    import os.path as op

    with open(in_file) as file:
        scalar_streamlines = [line.rstrip('\n') for line in file]

    # Read in data
    scalar_data = []
    for streamline in scalar_streamlines:
        scalar_data.append(streamline.split())

    del scalar_streamlines

    # Write values to file line-by-line
    out_file = op.join(wdir, "scalar.txt")
    f = open(out_file, "w+")
    for streamline in scalar_data:
        for data in streamline:
            f.write(data + "\n")
    f.close()

    del scalar_data

    return out_file

def writeScalar(wdir=None):
    writeScalar = pe.Node(niu.Function(function=_writeScalar,
                                       input_names=['in_file',
                                                    'wdir'],
                                       output_names=['out_file']),
                                       name="writeScalar")
    writeScalar.base_dir = wdir
    writeScalar.inputs.wdir = wdir

    return writeScalar
