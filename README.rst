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

- The global language attribute is set according to the subsite language. This overrides the plone negotiator. So if you set a language on a document in a susbite and enable content language negotiator, it will have no effect at all. A document in a plone site will still work as expected.

- Custom CSS for a Subsite

- Custom Logo for a Subsite. The logo is registered with a different name `subsite.logo`.
  The setup of `ftw.subsite` hides the default plone logo. You can change this afterwards
  if you like.


Compatibility
-------------

Plone 4.3 + Dexterity + Migration

With ``ftw.subsite`` 2.x only the AT based Subsite content is replaced with a
Dexterity based Subsite content + ftw.simplelayout default page. Thus the
Subsite portlet column, column renderer and the teaser portlet are no longer used and will be removed with ``ftw.subsite`` 2.1.0. The ``ftw.subsite`` release 2.0.x will provide a inplace migration. Be aware only static text portlets and subsite teaser portlets will be migrated. You need to provide your own migration for other portlets.
The subsite_view will be available in ``ftw.subsite`` 2.0.x and removed in 2.1.x.

The Archetypes to Dexterity migration has been rewritten in 2.1.1 and uses the inplace migrator
introduced in `ftw.upgrade` 2.0.0. The existing upgrade step has been rewritten in order to run
only when not yet migrated. The migrator is configured to not migrate fields which we had on AT
but no longer on DX. Instead, those values are backed up in the annotations of the new
subsite. For projects which add behaviors to the subsite for those old fields, the values can
be gotten from the annotations and re-set after applying the behavior. This is the responsibility
of the integration project.

Note about versions:

This package provides a version.cfg. Please make sure you are using suitable versions of `plone.app.contenttypes` and `plone.app.event`.

Currently it's recommend to use:

- plone.app.contenttypes 1.1b5: This is the latest 1.x release. 1.2.x is for Plone 5 and does not work.
- plone.app.event: 1.1.x supports Plone 4.3. Newer releases will require plone.app.widget, which also tries to install Plone 5.

.. image:: https://jenkins.4teamwork.ch/job/ftw.subsite-master-test-plone-4.3.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.subsite-master-test-plone-4.3.x.cfg



Plone 4.3

.. image:: https://jenkins.4teamwork.ch/job/ftw.subsite-1.x-test-plone-4.3.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.subsite-1.x-test-plone-4.3.x.cfg

Plone 4.2

.. image:: https://jenkins.4teamwork.ch/job/ftw.subsite-1.x-test-plone-4.2.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.subsite-1.x-test-plone-4.2.x.cfg

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

- Github: https://github.com/4teamwork/ftw.subsite
- Issues: https://github.com/4teamwork/ftw.subsite/issues
- Pypi: http://pypi.python.org/pypi/ftw.subsite
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.subsite


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.subsite`` is licensed under GNU General Public License, version 2.
