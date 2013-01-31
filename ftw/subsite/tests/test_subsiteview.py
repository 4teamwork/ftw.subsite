from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
import unittest2 as unittest
import transaction


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

    def test_view_render(self):
        self.browser.open(self.subsite.absolute_url())
        for item in range(1, 6):
            self.assertIn('<div id="subsite-column-%s" class="column">' % str(item), self.browser.contents)


    def test_manageview_render(self):
        self._auth()
        self.browser.open(self.subsite.absolute_url() + '/manage-subsiteview')
        for item in range(1, 6):
            self.assertIn('<div id="subsite-column-%s" class="column">' % str(item), self.browser.contents)
