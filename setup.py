from distutils.core import setup

setup(
    # Project information
    name='mrtrix_pipelines',
    version='1.0.0',
    description='Pipelines related to generating MRTrix tractography',
    packages=['mrtpipelines/interfaces',
              'mrtpipelines/workflows',
              'mrtpipelines/workflows/tractography'],
    scripts=['mrtpipelines/pipelines/genACTTractography'],

    # Metadata
    author='Jason Kai',
    author_email='tkai@uwo.ca',
    url='https://github.com/kaitj/mrtpipelines'
)
