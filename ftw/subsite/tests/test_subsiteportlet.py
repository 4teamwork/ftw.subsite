import unittest2 as unittest
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
import transaction


class TestSubsite(unittest.TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def tearDown(self):
        #self.portal.manage_delObjects(['mysubsite'])
        transaction.commit()

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
