from ftw.subsite.browser.subsiteview import SubsiteView
from ftw.subsite.interfaces import IFtwSubsiteLayer
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager
from zope.interface import alsoProvides
import os
import transaction
import unittest2 as unittest


class TestLogoViewlet(unittest.TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

    def _create_subsite(self):
        subsite = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'mysubsite',
            title="MySubsite"))

        transaction.commit()
        return subsite

    def _get_viewlet(self):
        subsite = self._create_subsite()
        alsoProvides(subsite.REQUEST, IFtwSubsiteLayer)
        view = SubsiteView(subsite, subsite.REQUEST)
        manager_name = 'plone.portalheader'
        manager = queryMultiAdapter(
            (subsite, subsite.REQUEST, view),
            IViewletManager,
            manager_name)
        self.failUnless(manager)
        # Set up viewlets
        manager.update()
        name = 'subsite.logo'
        return [v for v in manager.viewlets if v.__name__ == name]

    def tearDown(self):
        if 'mysubsite' in self.portal.objectIds():
            self.portal.manage_delObjects(['mysubsite'])
            transaction.commit()

    def test_component_registered(self):
        self.assertTrue(len(self._get_viewlet()) == 1)

    def test_without_logo(self):
        subsite = self._create_subsite()
        self._auth()
        self.browser.open(subsite.absolute_url())
        self.assertNotIn("%s/@@images" % subsite.absolute_url(),
                         self.browser.contents)

        self.assertNotIn('alt="MySubsite"', self.browser.contents)
        self.browser.open(self.portal.absolute_url())
        # No logo.png on subsite
        self.assertNotIn("%s/logo.png" % subsite.absolute_url(),
                         self.browser.contents)

        # There should be no change on plone root
        self.assertIn("%s/logo.png" % self.portal.absolute_url(),
                      self.browser.contents)

    def test_with_logo(self):
        subsite = self._create_subsite()
        file_ = open("%s/blue.png" % os.path.split(__file__)[0], 'r')
        file_.seek(0)
        subsite.setLogo(file_)
        transaction.commit()

        self._auth()
        self.browser.open(subsite.absolute_url())
        self.assertIn("%s/@@images" % subsite.absolute_url(),
                      self.browser.contents)

        self.assertIn('alt="MySubsite"', self.browser.contents)
        self.browser.open(self.portal.absolute_url())
        # No logo.png on subsite
        self.assertNotIn("%s/logo.png" % subsite.absolute_url(),
                         self.browser.contents)

        # There should be no change on plone root
        self.assertIn("%s/logo.png" % self.portal.absolute_url(),
                      self.browser.contents)

    def test_with_logo_subcontent(self):
        subsite = self._create_subsite()
        file_ = open("%s/blue.png" % os.path.split(__file__)[0], 'r')
        subsite.setLogo(file_)

        # Create more content
        folder = subsite.get(subsite.invokeFactory('Folder', 'folder'))
        folder1 = folder.get(folder.invokeFactory('Folder', 'folder'))

        transaction.commit()

        self._auth()
        self.browser.open(folder1.absolute_url())
        self.assertIn("%s/@@images" % subsite.absolute_url(),
                      self.browser.contents)

        self.assertIn('alt="MySubsite"', self.browser.contents)
        self.browser.open(self.portal.absolute_url())

        # There should be no change on plone root
        self.assertIn("%s/logo.png" % self.portal.absolute_url(),
                      self.browser.contents)

    def test_plone_logo_in_factory(self):
        self._auth()
        self.browser.open(
            self.portal.absolute_url() + '/createObject?type_name=Subsite')

        self.assertNotIn("/@@images/", self.browser.contents)

        self.assertIn("%s/logo.png" % self.portal.absolute_url(),
                      self.browser.contents)

    def test_logo_in_portal_tools(self):
        subsite = self._create_subsite()
        file_ = open("%s/blue.png" % os.path.split(__file__)[0], 'r')
        subsite.setLogo(file_)
        transaction.commit()
        self._auth()
        self.browser.open(subsite.absolute_url() + '/mail_password?userid=' + TEST_USER_ID)