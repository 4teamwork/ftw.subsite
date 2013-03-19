from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from ftw.subsite.testing import FTW_SUBSITE_SPECIAL_FUNCTIONAL_TESTING
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from zope.interface import alsoProvides
import unittest2 as unittest
import transaction
from zope.i18n.locales import locales
from Products.CMFCore.utils import getToolByName

class TestSubsiteForceLanguage(unittest.TestCase):

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

        #XXX setCookieEverywhere does not work - dont't know why

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
    def _set_language(self):
        """This Function is used to set the language of the plone site.
        We need this, because we wan't to make sure that the language is inherited when there isn't one forced.
        """
        locale = locales.getLocale('de')
        target_language = base_language = locale.id.language

        # If we get a territory, we enab le the combined language codes
        use_combined = False
        if locale.id.territory:
            use_combined = True
            target_language += '_' + locale.id.territory

            # As we have a sensible language code set now, we disable the
            # start neutral functionality

        tool = getToolByName(self.portal, "portal_languages")

        tool.manage_setLanguageSettings(target_language,
                                        [target_language],
                                        setUseCombinedLanguageCodes=use_combined,
                                        startNeutral=False)
        transaction.commit()

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

    def tearDown(self):
        if 'mysubsite' in self.portal.objectIds():
            self.portal.manage_delObjects(['mysubsite'])
            transaction.commit()

    def test_language_plone_root(self):
        self._auth()
        #Should have plone default language 'en'
        self.browser.open(self.portal.portal_url())
        link = self.browser.getLink('Site Map')
        self.assertIn(link.text, 'Site Map')

    def test_force_language_default(self):
        self._auth()
        subsite = self._create_subsite()  # No language

        # Plone default - 'en'
        self.browser.open(subsite.absolute_url())
        link = self.browser.getLink('Site Map')
        self.assertIn(link.text, 'Site Map')

    def test_force_language_change(self):
        self._auth()
        subsite = self._create_subsite(language='de')

        self.ltool.setLanguageBindings()
        transaction.commit()

        self.browser.open(subsite.absolute_url())
        link = self.browser.getLink('\xc3\x9cbersicht')
        self.assertIn(link.text, '\xc3\x9cbersicht')

    def test_force_language_change_subfolder(self):
        self._auth()
        subsite = self._create_subsite(language='de')
        folder = subsite.get(subsite.invokeFactory('Folder', 'folder'))

        self.ltool.setLanguageBindings()
        transaction.commit()

        self.browser.open(folder.absolute_url())
        link = self.browser.getLink('\xc3\x9cbersicht')
        self.assertIn(link.text, '\xc3\x9cbersicht')

    def test_force_language_change_subitem(self):
        self._auth()
        subsite = self._create_subsite(language='de')
        doc = subsite.get(subsite.invokeFactory('Document', 'document'))

        self.ltool.setLanguageBindings()
        transaction.commit()

        self.browser.open(doc.absolute_url())
        link = self.browser.getLink('\xc3\x9cbersicht')
        self.assertIn(link.text, '\xc3\x9cbersicht')

    def test_force_language_nav_root(self):
        # If there is a navigation root, which does not provide ISubsite
        # fallback to plone default
        folder = self.portal.get(self.portal.invokeFactory('Folder', 'folder'))
        alsoProvides(folder, INavigationRoot)
        transaction.commit()

        self.browser.open(folder.absolute_url())
        link = self.browser.getLink('Site Map')
        self.assertIn(link.text, 'Site Map')

    def test_language_inherited(self):
        """This test checks if the language is inherited correctly, if no language is forced on the subsite."""
        self._set_language()
        subsite = self._create_subsite(language='')
        self.browser.open(subsite.absolute_url())
        self.assertIn('Anmelden', self.browser.contents)



class TestNegotiatorSpecialCase(unittest.TestCase):

    # Do not setup ftw.subsite to test if the customized negotiator behaves
    # normal
    layer = FTW_SUBSITE_SPECIAL_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

    def test_subsitelayer_not_available(self):
        # The Subsite browserlayer is not available, so it should behave like
        # Plone default
        self.browser.open(self.portal.portal_url())
        link = self.browser.getLink('Site Map')
        self.assertIn(link.text, 'Site Map')
