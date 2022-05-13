from setuptools import setup, find_packages
from os import path

pkg_name = 'element_optogenetics'
here = path.abspath(path.dirname(__file__))

long_description = """"
DataJoint Element for Trial Based Optogenetics Experiments.
"""

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

with open(path.join(here, pkg_name, 'version.py')) as f:
    exec(f.read())

setup(
    name='element-optogenentics',
    version=__version__,
    description="DataJoint Element for Optogenetics",
    long_description=long_description,
    author='DataJoint',
    author_email='info@datajoint.com',
    license='MIT',
    url='https://github.com/datajoint/element-optogenetics',
    keywords='neuroscience optogenetics science datajoint',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    scripts=[],
    install_requires=requirements,
)
