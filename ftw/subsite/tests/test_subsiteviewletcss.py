from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login

from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager
from ftw.subsite.browser.subsiteview import SubsiteView
import unittest2 as unittest
import transaction


class TestSubsite(unittest.TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Reviewer', 'Contributor'])
        login(self.portal, TEST_USER_NAME)

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

        self.subsite = self._create_subsite()
        self.subsite.setAdditional_css('.column > div {color: red;}')
        transaction.commit()

    def _create_subsite(self):
        subsite = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'mysubsite',
            title="Peter"))
        transaction.commit()

        return subsite

    def _get_viewlet(self):
        view = SubsiteView(self.subsite, self.subsite.REQUEST)
        manager_name = 'plone.portaltop'
        manager = queryMultiAdapter(
            (self.subsite, self.subsite.REQUEST, view),
            IViewletManager,
            manager_name)
        self.failUnless(manager)
        # Set up viewlets
        manager.update()
        name = 'ftw.subsite.css'
        return [v for v in manager.viewlets if v.__name__ == name]

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

    def tearDown(self):
        self.portal.manage_delObjects(['mysubsite'])
        transaction.commit()

    def test_cssviewlet_in_subsite(self):
        self._auth()
        self.browser.open(self.subsite.absolute_url())
        self.assertIn('<style type="text/css" media="all">.column > div {color: red;}</style>', self.browser.contents)
        self.browser.open(self.portal.absolute_url())
        self.assertTrue('<style type="text/css" media="all">.column > div {color: red;}</style>' not in self.browser.contents)

    def test_component_registered(self):
        self.assertTrue(len(self._get_viewlet()) == 1)

    def test_cssviewlet_in_subfolder(self):
        folder = self.subsite.get(self.subsite.invokeFactory(
                'Folder',
                'myfolder',
                title="Hans"))
        transaction.commit()
        self._auth()
        self.browser.open(folder.absolute_url())
        self.assertIn('<style type="text/css" media="all">.column > div {color: red;}</style>', self.browser.contents)
