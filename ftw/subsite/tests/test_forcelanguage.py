from ftw.builder import Builder
from ftw.builder import create
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from ftw.subsite.testing import FTW_SUBSITE_SPECIAL_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase
from zope.i18n.locales import locales
import transaction


class TestSubsiteForceLanguage(TestCase):

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
        transaction.commit()

    def _set_language_de(self):
        """This Function is used to set the language of the plone site.
        We need this, because we wan't to make sure that the language is
        inherited when there isn't one forced.
        """
        locale = locales.getLocale('de')
        target_language = locale.id.language

        # If we get a territory, we enable the combined language codes
        use_combined = False
        if locale.id.territory:
            use_combined = True
            target_language += '_' + locale.id.territory

            # As we have a sensible language code set now, we disable the
            # start neutral functionality

        tool = getToolByName(self.portal, "portal_languages")

        tool.manage_setLanguageSettings(
            target_language,
            [target_language],
            setUseCombinedLanguageCodes=use_combined,
            startNeutral=False)
        transaction.commit()

    @browsing
    def test_language_plone_root(self, browser):
        browser.login().visit()
        # Grap some translated shizzle on the plone root site -
        # like site actions
        self.assertEquals(browser.css('#portal-siteactions').text,
                          ['Site Map Accessibility Contact'])

    @browsing
    def test_inherit_language_from_plone_root(self, browser):
        subsite = create(Builder('subsite').titled(u'A Subsite'))
        browser.login().visit(subsite)
        self.assertEquals(['Site Map Accessibility Contact'],
                          browser.css('#portal-siteactions').text)

    @browsing
    def test_change_language_to_de_on_subsite(self, browser):
        subsite = create(Builder('subsite')
                         .titled(u'Subsite')
                         .with_language('de'))
        self.ltool.setLanguageBindings()
        transaction.commit()

        browser.login().visit(subsite)
        self.assertEquals([u'\xdcbersicht Barrierefreiheit Kontakt'],
                          browser.css('#portal-siteactions').text,)

    @browsing
    def test_language_changed_to_de_also_on_subsite_subcontent(self, browser):
        subsite = create(Builder('subsite')
                         .titled(u'Subsite')
                         .with_language('de'))
        folder = create(Builder('folder').titled(u'A Folder').within(subsite))
        self.ltool.setLanguageBindings()
        transaction.commit()

        browser.login().visit(folder)
        self.assertEquals([u'\xdcbersicht Barrierefreiheit Kontakt'],
                          browser.css('#portal-siteactions').text)

    @browsing
    def test_language_inherited_on_subcontent_of_subsite(self, browser):
        self._set_language_de()
        subsite = create(Builder('subsite').titled(u'Subsite'))
        folder = create(Builder('folder').within(subsite))
        browser.login().visit(folder)
        self.assertEquals([u'\xdcbersicht Barrierefreiheit Kontakt'],
                          browser.css('#portal-siteactions').text)


class TestNegotiatorSpecialCase(TestCase):

    # Do not setup ftw.subsite to test if the customized negotiator behaves
    # normal
    layer = FTW_SUBSITE_SPECIAL_FUNCTIONAL_TESTING

    @browsing
    def test_subsitelayer_not_available(self, browser):
        # The Subsite browserlayer is not available, so it should behave like
        # Plone default
        folder = create(Builder('folder').titled(u'Subsite'))
        browser.login().visit(folder)
        self.assertEquals(['Site Map Accessibility Contact'],
                          browser.css('#portal-siteactions').text)
