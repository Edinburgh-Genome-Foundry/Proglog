import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

exec(open('proglog/version.py').read()) # loads __version__

setup(name='proglog',
      version=__version__,
      author='Zulko',
    description='Log and progress bar manager for console, notebooks, web...',
    long_description=open('README.rst').read(),
    license='MIT - copyright Edinburgh Genome Foundry',
    keywords="logger log progress bar",
    install_requires=['tqdm'],
    packages= find_packages(exclude='docs'))
