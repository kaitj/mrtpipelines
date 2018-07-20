from distutils.core import setup

setup(
    # Project information
    name='HCPTemplate_MRTrix_Pipeline',
    version='0.0.2',
    description='Pipeline to generate HCP UR100 Template using MRTrix3',
    packages=['mrtpipelines/interfaces',
              'mrtpipelines/workflows'],
    scripts=['mrtpipelines/pipelines/genHCPURTemplate'],

    # Metadata
    author='Jason Kai',
    author_email='tkai@uwo.ca',
    url='https://github.com/kaitj/mrtpipelines'
)
