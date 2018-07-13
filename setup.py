from distutils.core import setup

setup(
    # Project information
    name='HCPTemplate_MRTrix_Pipeline',
    version='0.0.1',
    description='Pipeline to generate HCP UR100 Template using MRTrix3',
    packages=['mrtpipelines/interfaces',
              'mrtpipelines/workflows',
              'mrtpipelines/workflows/tractography'],
    scripts=['mrtpipelines/pipelines/genACTTractography',
             'mrtpipelines/pipelines/genDhollanderTractography',
             'mrtpipelines/pipelines/genHCPURTemplate'],

    # Metadata
    author='Jason Kai',
    author_email='tkai@uwo.ca',
    url='https://github.com/kaitj/mrtpipelines'
)
