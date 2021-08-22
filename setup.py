#!/usr/bin/env python

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='blastsight',
    version='0.9.1',
    author='Gabriel Sanhueza',
    description='A 3D visualization library oriented to mining applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gsanhueza/BlastSight',
    packages=setuptools.find_packages(exclude=['tests*']),
    include_package_data=True,
    data_files=[
        ('share/applications', ['blastsight.desktop']),
        ('share/pixmaps', ['blastsight/view/gui/UI/icons/blastsight.png']),
    ],
    install_requires=[
        'numpy',
        'dxfgrabber',
        'PyOpenGL',
        'pandas',
        'qtpy',
        'h5py',
        'tables',
        'meshcut',
        'colour',
        'freetype-py',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    extras_require={
        'pyside2': ['pyside2'],
        'pyqt5': ['pyqt5'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

