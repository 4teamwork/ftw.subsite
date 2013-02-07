from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
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

        self.german.setSubsite_languages(self.french.UID())
        self.french.setSubsite_languages(self.german.UID())

        transaction.commit()

    def tearDown(self):
        self.portal.manage_delObjects(['mysubsite'])

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

    def test_language_switch(self):
        self._auth()
        self.browser.open(self.german.absolute_url())




    def test_languageswitch_functional(self):
        self.browser.open(self.subsite.absolute_url())
        self.browser.getLink('French').click()
        self.assertEqual(self.browser.url, self.portal.absolute_url()+'/fr')

    def test_languageswitch_no_existing_subsite_for_lang(self):
        self.browser.open(self.subsite.absolute_url())
        self.browser.getLink("German").click()
        self.assertEqual(self.browser.url, self.subsite.absolute_url())

    def test_languageswitch_set_language_not_set(self):
        self.browser.open(self.subsite.absolute_url() + '/switchLanguage?set_language=')
        self.assertEqual(self.browser.url, self.subsite.absolute_url())

    def test_languageswitch_set_language_not_set_cookielang(self):
        #This test is required to check if it works with the cookielang.
        #XXX: Somehow, we seem to be missing the languagecookie.
        #We should fix this, so we can test this situation as well
        self.browser.open(self.subsite.absolute_url() + '/switchLanguage?set_language=fr')
        self.browser.cookies['I18N_LANGUAGE'] = 'fr'
        self.browser.cookies.update()
        self.browser.open(self.subsite.absolute_url() + '/switchLanguage?set_language=')
        self.assertEqual(self.browser.url, self.fr.absolute_url())

    def test_languageswitch_wrong_param(self):
        self.browser.open(self.subsite.absolute_url() + '/switchLanguage?hans_peter=linder')
        self.assertEqual(self.browser.url, self.subsite.absolute_url())

    def test_langselector_no_show(self):
        self.browser.open(self.fr.absolute_url())
        self.assertTrue('switchLanguage' not in self.browser.contents)

    def test_langselector_show_with_subsite_languages(self):
        self.fr.setSubsite_languages(['de', 'fr'])
        transaction.commit()
        self.browser.open(self.fr.absolute_url())
        self.assertIn('switchLanguage', self.browser.contents)
