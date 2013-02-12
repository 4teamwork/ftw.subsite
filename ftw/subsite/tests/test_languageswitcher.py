from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from mechanize._mechanize import LinkNotFoundError
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
import unittest2 as unittest
import transaction


class TestLanguageswitcher(unittest.TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

        setRoles(self.portal, TEST_USER_ID,
                 ['Manager', 'Reviewer', 'Contributor'])
        login(self.portal, TEST_USER_NAME)
        self.german = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'germansubsite',
            title="German Subsite",
            forcelanguage="de"))

        self.french = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'French Subsite',
            title="frenchsubsite",
            forcelanguage="fr"))

        self.german.setLanguage_references(self.french.UID())
        self.french.setLanguage_references(self.german.UID())

        transaction.commit()

    def tearDown(self):
        if 'germansubsite' in self.portal.objectIds():
            self.portal.manage_delObjects(['germansubsite'])
        if 'frenchsubsite' in self.portal.objectIds():
            self.portal.manage_delObjects(['frenchsubsite'])
        transaction.commit()

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

    def test_language_switch(self):
        self._auth()
        self.browser.open(self.german.absolute_url())

        link = self.browser.getLink('French')
        self.assertTrue(link)
        link.click()
        self.assertEquals(self.browser.url, self.french.absolute_url())

        link = self.browser.getLink('German')
        self.assertTrue(link)
        link.click()
        self.assertEquals(self.browser.url, self.german.absolute_url())

    def test_language_switch_available(self):
        self.german.setLanguage_references([])
        transaction.commit()

        self._auth()
        self.browser.open(self.german.absolute_url())
        self.assertRaises(LinkNotFoundError, self.browser.getLink, 'French')

        self.browser.open(self.portal.portal_url())
        self.assertRaises(LinkNotFoundError, self.browser.getLink, 'French')

    def test_language_switch_multiple_sites(self):
        self.italy = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'Italian Subsite',
            title="italiansubsite",
            forcelanguage="it"))

        self.german.setLanguage_references(
            [self.french.UID(), self.italy.UID()])
        transaction.commit()

        self.browser.open(self.german.absolute_url())
        self.assertTrue(self.browser.getLink('French'))
        self.assertTrue(self.browser.getLink('Italian'))

    def test_language_switch_multiple_sites_no_lang_set(self):
        self.italy = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'Italian Subsite',
            title="italiansubsite"))

        self.german.setLanguage_references(
            [self.french.UID(), self.italy.UID()])
        transaction.commit()

        self.browser.open(self.german.absolute_url())
        self.assertTrue(self.browser.getLink('French'))
        self.assertRaises(LinkNotFoundError, self.browser.getLink, 'Italian')
