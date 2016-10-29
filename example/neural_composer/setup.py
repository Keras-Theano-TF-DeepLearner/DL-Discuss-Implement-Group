# coding: utf-8

import os

from distutils.core import setup


__version__ = '0.01'

short_description = 'Composing music with pre-trained neural network.'

try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = short_description


install_requires = [
    'Django>=1.9',
    'celery>=3.1.20',
    'h5py>=2.5.0',
    'music21>=2.2.1',
    'keras>=0.3.2',
    'redis>=2.10.5',
    'requests>=2.9.1'
]

setup(
    name='neural_composer',
    packages=['composer'],
    version=__version__,
    description=short_description,
    long_description=long_description,
    author='Alexander Zhebrak',
    author_email='fata2ex@gmail.com',
    license='MIT',
    url='https://github.com/fata1ex/neural_composer',
    download_url='https://github.com/fata1ex/neural_composer',
    keywords=['django', 'neural network', 'music'],
    install_requires=install_requires,
    zip_safe=False,
    include_package_data=True,
    classifiers=[],
)
