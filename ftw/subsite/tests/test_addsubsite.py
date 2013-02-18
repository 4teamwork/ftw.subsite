from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from pyquery import PyQuery as pq
import transaction
import unittest2 as unittest


class TestSubsite(unittest.TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

    def tearDown(self):
        if 'testsubsite' in self.portal.objectIds():
            self.portal.manage_delObjects(['testsubsite'])
            transaction.commit()

    def test_fti(self):
        self.assertIn('Subsite', self.portal.portal_types.objectIds())

    def test_subsite_addable(self):
        self._auth()
        self.browser.open(
            self.portal.absolute_url() + '/createObject?type_name=Subsite')
        factory_url = self.browser.url[:-5]  # Remove "/edit"
        self.assertIn('portal_factory', factory_url)

        # Send form empty
        self.browser.getControl('Save').click()
        # Stay on add form
        self.assertIn(factory_url, self.browser.url)

        doc = pq(self.browser.contents)

        # Title is required
        input_field = doc('input#title').parents('.field')
        self.assertTrue(input_field, 'Title field not found')
        self.assertIn('error', input_field.attr('class').split(' '),
                      'Title seems not to be required, but should be')

        # Set title and submit form
        self.browser.getControl(name="title").value = "Testsubsite"
        self.browser.getControl("Save").click()

        self.assertIn('testsubsite', self.portal.objectIds())
        self.assertEquals(self.browser.url,
                          "%s/testsubsite/" % self.portal.absolute_url())
