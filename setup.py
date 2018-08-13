from distutils.core import setup

setup(
    # Project information
    name='MRTrix_Pipeline',
    version='0.0.1',
    description='Pipelines related to generating MRTrix tractography',
    packages=['mrtpipelines/interfaces',
              'mrtpipelines/workflows'],
    scripts=['mrtpipelines/pipelines/genACTTractography',
             'mrtpipelines/pipelines/genDhollanderTractography'],

    # Metadata
    author='Jason Kai',
    author_email='tkai@uwo.ca',
    url='https://github.com/kaitj/mrtpipelines'
)
