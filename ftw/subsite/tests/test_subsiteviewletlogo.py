from ftw.builder import Builder
from ftw.builder import create
from ftw.subsite.browser.subsiteview import SubsiteView
from ftw.subsite.interfaces import IFtwSubsiteLayer
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.namedfile.file import NamedBlobImage
from plone.app.testing import TEST_USER_ID
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

    def assert_subsite_logo_src(self, browser):
        img_src = browser.css('#portal-logo img').first.attrib['src']
        expected_part_image_src = '{0}/@@images/'.format(
            self.subsite.absolute_url())
        assert img_src.startswith(expected_part_image_src), (
            'Wrong logo path, expect img src starting with: {0}'.format(
                expected_part_image_src))

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
        file_ = open("%s/blue.png" % os.path.split(__file__)[0], 'r')
        file_.seek(0)
        self.subsite.logo = NamedBlobImage(data=file_.read(),
                                           filename=u'logo.png')
        transaction.commit()

        browser.login().visit(self.subsite)

        self.assertEquals(self.subsite.absolute_url(),
                          browser.css('#portal-logo').first.attrib['href'])

        self.assert_subsite_logo_src(browser)

        browser.visit(self.portal)
        self.assertEquals('http://nohost/plone/logo.png',
                          browser.css('#portal-logo img').first.attrib['src'])

    @browsing
    def test_with_logo_subcontent(self, browser):
        file_ = open("%s/blue.png" % os.path.split(__file__)[0], 'r')
        file_.seek(0)
        self.subsite.logo = NamedBlobImage(data=file_.read(),
                                           filename=u'logo.png')
        transaction.commit()

        subfolder = create(Builder('folder').within(self.subsite))
        subsubfolder = create(Builder('folder').within(subfolder))

        browser.login().visit(subsubfolder)
        self.assert_subsite_logo_src(browser)

    @browsing
    def test_logo_in_portal_tools(self, browser):
        file_ = open("%s/blue.png" % os.path.split(__file__)[0], 'r')
        file_.seek(0)
        self.subsite.logo = NamedBlobImage(data=file_.read(),
                                           filename=u'logo.png')
        transaction.commit()
        browser.login().visit(self.subsite,
                              view='mail_password',
                              data={'userid': TEST_USER_ID})

        self.assert_subsite_logo_src(browser)
