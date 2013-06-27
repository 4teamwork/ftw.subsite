from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.testing.z2 import Browser
from pyquery import PyQuery
import transaction
import unittest2 as unittest


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

        link = self.browser.getLink('Fran\xc3\xa7ais')
        self.assertTrue(link)
        link.click()
        self.assertEquals(self.browser.url, self.french.absolute_url())

        link = self.browser.getLink('Deutsch')
        self.assertTrue(link)
        link.click()
        self.assertEquals(self.browser.url, self.german.absolute_url())

    def test_language_switch_available(self):
        self.german.setLanguage_references([])
        transaction.commit()

        self._auth()
        self.assertSelectableLanguagesOnPage(
            [],
            self.german.absolute_url())

        self.assertSelectableLanguagesOnPage(
            [],
            self.portal.absolute_url())

    def test_language_switch_multiple_sites(self):
        self.italy = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'Italian Subsite',
            title="italiansubsite",
            forcelanguage="it"))

        self.german.setLanguage_references(
            [self.french.UID(), self.italy.UID()])
        transaction.commit()

        self.assertSelectableLanguagesOnPage(
            [u'Fran\xe7ais', u'Italiano'],
            self.german.absolute_url())

    def test_language_switch_multiple_sites_no_lang_set(self):
        self.italy = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'Italian Subsite',
            title="italiansubsite"))

        self.german.setLanguage_references(
            [self.french.UID(), self.italy.UID()])
        transaction.commit()

        self.assertSelectableLanguagesOnPage(
            [u'Fran\xe7ais'],
            self.german.absolute_url())

    def test_listing_plone_site_and_language_references_combined(self):
        self.assertSelectableLanguagesOnPage(
            [u'Fran\xe7ais'],
            self.german.absolute_url())

        self.german.setLinkSiteInLanguagechooser(True)
        transaction.commit()

        self.assertSelectableLanguagesOnPage(
            [u'Fran\xe7ais', u'English'],
            self.german.absolute_url())

    def test_listing_only_plone_site(self):
        self.german.setLinkSiteInLanguagechooser(True)
        self.german.setLanguage_references([])
        transaction.commit()

        self.assertSelectableLanguagesOnPage(
            [u'English'],
            self.german.absolute_url())

    def assertSelectableLanguagesOnPage(self, expected_languages, url):
        self.browser.open(url)
        doc = PyQuery(self.browser.contents)
        self.assertEquals(
            set(expected_languages),
            set([link.text for link in doc('#portal-languageselector a')]))
