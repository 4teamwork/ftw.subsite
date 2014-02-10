from setuptools import setup, find_packages
import os

version = '1.3.1'

tests_require = [
    'plone.app.testing',
    'plone.app.portlets',
    'collective.mockmailhost',
    'pyquery',
    'ftw.testing [splinter]',
    'ftw.builder',
    ]

setup(name='ftw.subsite',
      version=version,
      description="",
      long_description=open('README.rst').read() + '\n' +
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw subsite',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.subsite',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'plone.formwidget.contenttree',
        'plone.namedfile',
        'plone.formwidget.namedfile',
        # -*- Extra requirements: -*-
        ],

      tests_require=tests_require,
      extras_require={'tests': tests_require},

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
