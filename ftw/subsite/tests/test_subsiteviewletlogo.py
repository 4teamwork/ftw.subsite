from ftw.builder import Builder
from ftw.builder import create
from ftw.subsite.browser.subsiteview import SubsiteView
from ftw.subsite.interfaces import IFtwSubsiteLayer
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobImage
from unittest2 import TestCase
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager
import os
import transaction


class TestLogoViewlet(TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        self.subsite = create(Builder('subsite').titled(u'MySubsite'))

    def _get_viewlet(self):
        alsoProvides(self.subsite.REQUEST, IFtwSubsiteLayer)
        view = SubsiteView(self.subsite, self.subsite.REQUEST)
        manager_name = 'plone.portalheader'
        manager = queryMultiAdapter(
            (self.subsite, self.subsite.REQUEST, view),
            IViewletManager,
            manager_name)
        self.failUnless(manager)
        # Set up viewlets
        manager.update()
        name = 'subsite.logo'
        return [v for v in manager.viewlets if v.__name__ == name]

    def _add_logo(self, subsite):
        file_ = open("%s/blue.png" % os.path.split(__file__)[0], 'r')
        file_.seek(0)
        subsite.logo = NamedBlobImage(data=file_.read(),
                                      filename=u'logo.png')
        transaction.commit()

    def assert_subsite_logo_src(self, browser):
        img_src = browser.css('#portal-logo img').first.attrib['src']
        expected_part_image_src = '{0}/@@images/'.format(
            self.subsite.absolute_url())
        assert img_src.startswith(expected_part_image_src), (
            'Wrong logo path, expect img src starting with: {0}'.format(
                expected_part_image_src))

    def test_component_registered(self):
        self.assertTrue(len(self._get_viewlet()) == 1)

    @browsing
    def test_without_logo(self, browser):
        browser.login().visit(self.subsite)

        self.assertEquals(self.subsite.absolute_url(),
                          browser.css('#portal-logo').first.attrib['href'])

        self.assertEquals('http://nohost/plone/logo.png',
                          browser.css('#portal-logo img').first.attrib['src'])

        browser.visit(self.portal)
        self.assertEquals('http://nohost/plone/logo.png',
                          browser.css('#portal-logo img').first.attrib['src'])

    @browsing
    def test_with_logo(self, browser):
        self._add_logo(self.subsite)

        browser.login().visit(self.subsite)

        self.assertEquals(self.subsite.absolute_url(),
                          browser.css('#portal-logo').first.attrib['href'])

        self.assert_subsite_logo_src(browser)

        browser.visit(self.portal)
        self.assertEquals('http://nohost/plone/logo.png',
                          browser.css('#portal-logo img').first.attrib['src'])

    @browsing
    def test_with_logo_subcontent(self, browser):
        self._add_logo(self.subsite)

        subfolder = create(Builder('folder').within(self.subsite))
        subsubfolder = create(Builder('folder').within(subfolder))

        browser.login().visit(subsubfolder)
        self.assert_subsite_logo_src(browser)

    @browsing
    def test_logo_in_portal_tools(self, browser):
        self._add_logo(self.subsite)

        browser.login().visit(self.subsite,
                              view='mail_password',
                              data={'userid': TEST_USER_ID})

        self.assert_subsite_logo_src(browser)

    @browsing
    def test_logo_img_tag_has_no_title_attribute(self, browser):
        self._add_logo(self.subsite)

        browser.login().visit(self.subsite)

        self.assertIsNone(
            browser.css('#portal-logo img').first.attrib.get('title', None))

    @browsing
    def test_logo_img_tag_has_no_alt_attribute_if_empty(self, browser):
        self._add_logo(self.subsite)

        browser.login().visit(self.subsite)

        self.assertIsNone(
            browser.css('#portal-logo img').first.attrib.get('alt', None))

    @browsing
    def test_logo_img_tag_has_alt_attribute_if_filled(self, browser):
        subsite = create(Builder('subsite')
                         .titled(u'My Subsite')
                         .having(logo_alt_text=u'My alt text'))
        self._add_logo(subsite)

        browser.login().visit(subsite)

        self.assertEqual(
            u'My alt text',
            browser.css('#portal-logo img').first.attrib['alt'])

        # Make sure the image has an alt text for non-subsites.
        self.portal._setProperty('logo_alt_text', 'Plone Logo Alt Text',
                                 'string')
        transaction.commit()
        browser.visit(self.portal)
        self.assertEqual(
            u'Plone Logo Alt Text',
            browser.css('#portal-logo img').first.attrib['alt'])

