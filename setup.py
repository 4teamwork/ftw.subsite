from setuptools import setup, find_packages
import os

version = '1.0'

tests_require = [
    'plone.app.testing',
    ]

long_description = (
    open('README.rst').read()
    + '\n' +
    open('docs/HISTORY.txt').read()
    + '\n')

setup(name='ftw.subsite',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://github.com/4teamwork/ftw.subsite',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.formwidget.contenttree',
          # -*- Extra requirements: -*-
      ],

      tests_require=tests_require,
      extras_require={'tests': tests_require},

      entry_points="""
      # -*- Entry points: -*-
      """,
      )
