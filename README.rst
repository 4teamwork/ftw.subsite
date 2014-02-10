ftw.subsite
===========

``ftw.subsite`` provides a ``Subsite`` content type for embedding another website
within a Plone site.
It does this by defining it as navigation root.


Additional functionality provided by `ftw.subsite`
--------------------------------------------------

- It is possible to define a language on a subsite content, which overrides the
  default behavior of how Plone deals with languages (PloneLanguageTool).
  If you define a language on a subsite all content on and in the
  subsite will be delivered in the chosen language. This functionality
  is not related to the product LinguaPlone.

  Make sure you have all languages activated you want, for example:

  .. code:: ini

      environment-vars =
          PTS_LANGUAGES de en fr
          zope_i18n_allowed_languages de en fr


- ``ftw.subsite`` has its own language switch viewlet which is based
  on the Subsite configuration. You can connect two or more subsites with
  different languages together by referencing each other with the custom
  reference field on the Subsite.

- Custom CSS for a Subsite

- Custom Logo for a Subsite. The logo is registered with a different name `subsite.logo`.
  The setup of `ftw.subsite` hides the default plone logo. You can change this afterwards
  if you like.


Compatibility
-------------

Plone 4.3

.. image:: https://jenkins.4teamwork.ch/job/ftw.subsite-master-test-plone-4.3.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.subsite-master-test-plone-4.3.x.cfg

Plone 4.2

.. image:: https://jenkins.4teamwork.ch/job/ftw.subsite-master-test-plone-4.2.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.subsite-master-test-plone-4.2.x.cfg

**Important**

Plone 4.1 support has been dropped due to Plonebugs which interfere with our testsetup
which were fixed in Plone 4.2.

Last Version of ftw.subsite to support Plone 4.1 is 1.3.0.

Usage
-----

- Add ``ftw.subsite`` to your buildout configuration:

.. code:: ini

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

.. image:: https://cruel-carlota.pagodabox.com/fc72df1ade53c50967d1f08b8dbbfe4e
   :alt: githalytics.com
   :target: http://githalytics.com/4teamwork/ftw.subsite
