from setuptools import setup, find_packages

setup(name='mel-scripts-genclassfile',
  version='0.0.1dev',
  description='generate c++ class file from the command line',
  author='Meleneth',
  author_email='meleneth@gmail.com',
  license='GPL',
  packages=find_packages('src'),
  package_dir={'': 'src'},
  install_requires=[],
  tests_require=['pytest', 'pytest-cov'],
  entry_points = {
    'console_scripts': [
      'genclassfile=mel.scripts.genclassfile.commandline:main'
    ]
  },
  zip_safe=False
)

