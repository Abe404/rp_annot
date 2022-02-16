from setuptools import setup
from pathlib import Path

current_dir = Path(__file__).parent
long_description = (current_dir / "README.md").read_text()

setup(
  name = 'rp_annot',
  packages = ['rp_annot'],
  version = '0.0.4',
  license = 'GPLv3', 
  description = 'Minimal compression library for sparse or contiguous 1D numpy boolean arrays',
  long_description_content_type='text/markdown',
  long_description=long_description,
  author = 'Abraham George Smith',
  author_email = 'abe@abesmith.co.uk',
  url = 'https://github.com/Abe404/rp_annot',
  download_url = 'https://github.com/Abe404/rp_annot/archive/refs/tags/0.0.4.tar.gz',
  keywords = ['numpy', 'compression', 'sparse', 'boolean'],
  install_requires=[
      "numpy >=1.18.2",
  ],
  classifiers=[
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent'
  ]
)
