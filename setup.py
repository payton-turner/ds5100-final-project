from setuptools import setup, find_packages

setup(
    name='montecarlo',
    version='1.0.0',
    url='https://github.com/payton-turner/ds5100-final-project.git',
    author='Payton turner',
    author_email='wdc9um@virginia.edu',
    description='A Monte Carlo simulator package with Die, Game, and Analyzer classes.',
    packages=find_packages(),    
    install_requires=['numpy', 'pandas']
)
