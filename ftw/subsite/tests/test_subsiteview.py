from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from zope.component import queryMultiAdapter
import unittest2 as unittest
import transaction
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import login


class TestSubsite(unittest.TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

        self.subsite = self._create_subsite()

        transaction.commit()

    def _create_subsite(self):
        subsite = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'mysubsite',
            title="Peter"))
        transaction.commit()

        return subsite

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

    def tearDown(self):
        self.portal.manage_delObjects(['mysubsite'])
        transaction.commit()

    def test_view_has_permission(self):
        view = queryMultiAdapter((self.subsite, self.portal.REQUEST), name="subsite_view")
        logout()
        self.assertFalse(view.hasPermissions())
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        login(self.portal, TEST_USER_NAME)
        self.assertFalse(view.hasPermissions())
        logout()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.assertTrue(view.hasPermissions())

    def test_view_render(self):
        self.browser.open(self.subsite.absolute_url())
        for item in range(1, 6):
            self.assertIn('<div id="subsite-column-%s" class="column">' % str(item), self.browser.contents)


    def test_manageview_render(self):
        self._auth()
        self.browser.open(self.subsite.absolute_url() + '/manage-subsiteview')
        for item in range(1, 6):
            self.assertIn('<div id="subsite-column-%s" class="column">' % str(item), self.browser.contents)
