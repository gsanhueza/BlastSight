import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='minevis',
    version='0.1.0',
    author='Gabriel Sanhueza',
    description='3D visualization software designed to aid in Mining research.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gsanhueza/MineVis',
    packages=setuptools.find_packages(),
,   include_package_data=True
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
