ftw.subsite
===========

``ftw.subsite`` provides a ``Subsite`` content type for embedding another website
within a Plone site.
It does this by defining it as navigation root.


Aditional functionality provided by ``ftw.subsite``
---------------------------------------------------

- It's possible to define a language on a subsite, which overrides the
  default behavior of how Plone deals with languages (PloneLanguageTool)
  If you define a language on a subsite all content on and in the
  subsite will be delivered with the chosen language. This functionality
  has nothing to do with LinguaPlone

  Be sure you have activated the language you want, for example:

  ::

      environment-vars =
          PTS_LANGUAGES de en fr
          zope_i18n_allowed_languages de en fr


- ``ftw.subsite`` has his own language switch viewlet, it's based
  on the Subsite configuration. You can connect two or more subsites with
  diffrent languages together by referencing each other with the custom
  reference field on the Subsite.

- Custom CSS for a Ssubsite

- Custom Logo for a Subsite

Usage
-----

- Add ``ftw.subsite`` to your buildout configuration:

::

    [instance]
    eggs +=
        ftw.subsite

- Install the generic import profile.


Links
-----

- Main github project repository: https://github.com/4teamwork/ftw.subsite
- Issue tracker: https://github.com/4teamwork/ftw.subsite/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.subsite
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.subsite


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.subsite`` is licensed under GNU General Public License, version 2.
