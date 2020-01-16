from distutils.core import setup
from mrtpipelines._version import __version__

setup(
    # Project information
    name='MRTrix3 Pipeline',
    version=__version__,
    description='Pipelines related to generating MRTrix tractography',
    packages=['mrtpipelines',
              'mrtpipelines/interfaces',
              'mrtpipelines/workflows'],
    scripts=['mrtpipelines/pipelines/genDhollanderTractography',
             'mrtpipelines/pipelines/tractScalar'],

    # Metadata
    author='Jason Kai',
    author_email='tkai@uwo.ca',
    url='https://github.com/kaitj/mrtpipelines'
)
