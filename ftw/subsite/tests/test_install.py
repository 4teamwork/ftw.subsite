import unittest2 as unittest
from ftw.subsite.testing import FTW_SUBSITE_INTEGRATION_TESTING
from plone.testing.z2 import Browser
from plone.app.testing import login, TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD, setRoles
import transaction
from plone.app.blob.tests.utils import makeFileUpload
from StringIO import StringIO
from base64 import decodestring


class TestSubsite(unittest.TestCase):

    layer = FTW_SUBSITE_INTEGRATION_TESTING

    def test_add_subsite(self):
        portal = self.layer['portal']
        browser = Browser(self.layer['app'])
        browser.handleErrors = False
        setRoles(portal, TEST_USER_ID, ['Manager', 'Reviewer', 'Contributor'])
        transaction.commit()
        browser.open(portal.absolute_url() + '/login_form')
        browser.getControl(name='__ac_name').value = TEST_USER_NAME
        browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        browser.getControl(name='submit').click()
        browser.open(portal.absolute_url() + '/folder_factories')
        button = browser.getControl(name="url")
        button.value = [button.options[-1]]
        browser.getControl(name="form.button.Add").click()
        file_ = open("../../ftw/subsite/tests/blue.png")
        file_field = browser.getControl(name="logo_file")
        file_field.add_file(StringIO(file_.read()), 'image/png', 'blue.png')
        browser.getControl(name="title").value = "Testsubsite"
        browser.getControl(name="form.button.save").click()
        self.assertEqual(browser.url, 'http://nohost/plone/testsubsite/')

    def test_logo_viewlet(self):
        portal = self.layer['portal']
        browser = Browser(self.layer['app'])
        browser.handleErrors = False
        file_ = open("../../ftw/subsite/tests/blue.png")
        portal.invokeFactory(
            'Subsite', 'mysubsite', title="Peter", logo=file_.read())
        setRoles(portal, TEST_USER_ID, ['Manager', 'Reviewer', 'Contributor'])
        transaction.commit()
        browser.open(portal.absolute_url() + '/login_form')
        browser.getControl(name='__ac_name').value = TEST_USER_NAME
        browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        browser.getControl(name='submit').click()
        browser.open(portal.absolute_url() + '/mysubsite')
        self.assertTrue(
            'http://nohost/plone/mysubsite/@@images' in browser.contents)
        self.assertTrue('alt="Peter"' in browser.contents)
        browser.open(portal.absolute_url())
        self.assertTrue("http://nohost/plone/logo.png" in browser.contents)

    def test_portlets(self):
        portal = self.layer['portal']
        browser = Browser(self.layer['app'])
        browser.handleErrors = False
        file_ = open("../../ftw/subsite/tests/blue.png")
        portal.invokeFactory(
            'Subsite', 'another', title="Peter", logo=file_.read())
        setRoles(portal, TEST_USER_ID, ['Manager', 'Reviewer', 'Contributor'])
        transaction.commit()
        browser.open(portal.absolute_url() + '/another')
        self.assertTrue('edit dashboard' not in browser.contents)
        browser.open(portal.absolute_url() + '/login_form')
        browser.getControl(name='__ac_name').value = TEST_USER_NAME
        browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        browser.getControl(name='submit').click()
        browser.open(portal.absolute_url() + '/another')
        self.assertTrue('edit dashboard' in browser.contents)
        browser.open('http://nohost/plone/another/@@manage-subsiteview')
        self.assertTrue('dashboard-portlets1' in browser.contents)
        self.assertTrue('dashboard-portlets2' in browser.contents)
        self.assertTrue('dashboard-portlets3' in browser.contents)
        self.assertTrue('dashboard-portlets4' in browser.contents)
        self.assertTrue('dashboard-portlets5' in browser.contents)
        self.assertTrue('dashboard-portlets6' in browser.contents)
