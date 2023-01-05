#!/usr/bin/env python3

from setuptools import setup

setup(name='WGapplet',
      version='0.1',
      description='An applet for wire-guard connections',
      url='https://github.com/mkampl/WGapplet',
      author='Markus Kampl',
      author_email='markus.kampl@gmail.com',
      license='?',
      install_requires=[
          'psutil',
          'notify2',
          'PyQt5',
      ],
      packages=['WGapplet'],
      scripts=['bin/wg-applet'],
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      include_package_data=True,
      zip_safe=False)
