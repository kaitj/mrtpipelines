from distutils.core import setup
from mrtpipelines._version import __version__

setup(
    # Project information
    name='MRTrix_TemplatePipeline',
    version=__version__,
    description='Pipeline to generate templates using MRTrix3',
    packages=['mrtpipelines',
              'mrtpipelines/interfaces',
              'mrtpipelines/workflows'],
    scripts=['mrtpipelines/pipelines/genHCPURTemplate',
             'mrtpipelines/pipelines/genTemplate',
             'mrtpipelines/pipelines/xfmTracts'],

    # Metadata
    author='Jason Kai',
    author_email='tkai@uwo.ca',
    url='https://github.com/kaitj/mrtpipelines/tree/template'
)
