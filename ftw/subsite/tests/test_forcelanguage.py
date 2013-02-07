from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from zope.interface import alsoProvides
import unittest2 as unittest
import transaction


class TestSubsite(unittest.TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        self.ltool = self.portal.portal_languages
        default = 'en'
        supported = ['en', 'de']
        self.ltool.manage_setLanguageSettings(
            default,
            supported,
            setUseCombinedLanguageCodes=False,
            # Set this only for better testing ability
            setCookieEverywhere=True)

        #XXX setCookieEverywhere does not work

        transaction.commit()

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def _create_subsite(self, language=None):
        subsite = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'mysubsite',
            title="My Subsite"))

        if language:
            subsite.setForcelanguage(language)
        transaction.commit()

        return subsite

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

    def tearDown(self):
        if 'mysubsite' in self.portal.objectIds():
            self.portal.manage_delObjects(['mysubsite'])
            transaction.commit()

    def test_language_plone_root(self):
        self._auth()
        self.browser.open(self.portal.portal_url())
        #Should have plone default language 'en'
        self.assertIn(
            '<html xmlns="http://www.w3.org/1999/xhtml" lang="en">',
            self.browser.contents)

    def test_force_language_default(self):
        self._auth()
        subsite = self._create_subsite()  # No language

        self.browser.open(subsite.absolute_url())
        # Plone default is en
        self.assertIn(
            '<html xmlns="http://www.w3.org/1999/xhtml" lang="en">',
            self.browser.contents)

    def test_force_language_change(self):
        self._auth()
        subsite = self._create_subsite(language='de')

        self.ltool.setLanguageBindings()
        transaction.commit()

        self.browser.open(subsite.absolute_url())
        self.assertIn(
            '<html xmlns="http://www.w3.org/1999/xhtml" lang="de">',
            self.browser.contents)

    def test_force_language_change_subfolder(self):
        self._auth()
        subsite = self._create_subsite(language='de')
        folder = subsite.get(subsite.invokeFactory('Folder', 'folder'))

        self.ltool.setLanguageBindings()
        transaction.commit()

        self.browser.open(folder.absolute_url())
        self.assertIn(
            '<html xmlns="http://www.w3.org/1999/xhtml" lang="de">',
            self.browser.contents)

    def test_force_language_change_subitem(self):
        self._auth()
        subsite = self._create_subsite(language='de')
        doc = subsite.get(subsite.invokeFactory('Document', 'document'))

        self.ltool.setLanguageBindings()
        transaction.commit()

        self.browser.open(doc.absolute_url())
        self.assertIn(
            '<html xmlns="http://www.w3.org/1999/xhtml" lang="de">',
            self.browser.contents)

    def test_force_language_nav_root(self):
        # If there is a navigation root, which does not provide ISubsite
        # fallback to plone default
        folder = self.portal.get(self.portal.invokeFactory('Folder', 'folder'))
        alsoProvides(folder, INavigationRoot)
        transaction.commit()

        self.browser.open(folder.absolute_url())
        self.assertIn(
            '<html xmlns="http://www.w3.org/1999/xhtml" lang="en">',
            self.browser.contents)
