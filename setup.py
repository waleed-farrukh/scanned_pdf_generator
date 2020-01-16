from setuptools import setup, find_packages
from os import path

setup(name='scanned-variant-generator',
      version = '0.1',
      description = 'Generating Scanned/Mobile-captured variants of a document',
      keywords = 'scanned',
      author='gini',
      install_requires = ['pyblur', 'opencv-python', 'click', 'Wand'],
      extras_require={
        'tests': ['pytest>=3.4.0,<4.0']},
      packages=find_packages(),
      package_data={
            'config' : ['config.json'],
            'variant_generator.resources.backgrounds': ['*.jpg']
      },
      zip_safe = False,
      scripts=['run.py'],
      entry_points=dict(console_scripts=['variant-generator=run:run'])
)