from ftw.builder import Builder
from ftw.builder import create
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from ftw.subsite.tests.pages import LanguageSwitcher
from ftw.testing import browser
from ftw.testing.pages import Plone
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from unittest2 import TestCase
import transaction


def introduce_language_subsites(*subsites):
    for subsite in subsites:
        uids = [obj.UID() for obj in subsites]
        uids.remove(subsite.UID())
        subsite.setLanguage_references(uids)

    transaction.commit()


class TestLanguageSwitcher(TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_shows_other_referenced_languages(self):
        german = create(Builder('subsite').with_language('de'))
        french = create(Builder('subsite').with_language('fr'))
        italian = create(Builder('subsite').with_language('it'))
        introduce_language_subsites(german, french, italian)

        Plone().login().visit(german)
        self.assertEquals([u'Fran\xe7ais', u'Italiano'],
                          LanguageSwitcher().languages)

    def test_going_to_another_language(self):
        german = create(Builder('subsite').with_language('de'))
        french = create(Builder('subsite').with_language('fr'))
        introduce_language_subsites(german, french)

        Plone().login().visit(german)
        LanguageSwitcher().click_language(u'Fran\xe7ais')
        self.assertEquals(french.absolute_url(), browser().url)
        LanguageSwitcher().click_language(u'Deutsch')
        self.assertEquals(german.absolute_url(), browser().url)

    def test_language_switch_invisible_unless_languages_hooked_up(self):
        german = create(Builder('subsite').with_language('de'))
        french = create(Builder('subsite').with_language('fr'))

        Plone().login().visit(german)
        self.assertFalse(LanguageSwitcher().available)
        introduce_language_subsites(german, french)
        Plone().visit(german)
        self.assertTrue(LanguageSwitcher().available)

    def test_other_site_not_visible_when_no_subsite_language_defined(self):
        german = create(Builder('subsite').with_language('de'))
        unkown = create(Builder('subsite').titled('unkown'))
        introduce_language_subsites(german, unkown)

        Plone().login().visit(german)
        self.assertEquals([], LanguageSwitcher().languages)

    def test_does_not_show_subsites_of_other_language_groups(self):
        german = create(Builder('subsite').with_language('de'))
        french = create(Builder('subsite').with_language('fr'))
        italian = create(Builder('subsite').with_language('it'))
        spanish = create(Builder('subsite').with_language('es'))

        introduce_language_subsites(german, french)
        introduce_language_subsites(italian, spanish)

        Plone().login()

        self.assertEquals(
            {'german': [u'Fran\xe7ais'],
             'french': [u'Deutsch'],
             'italian': [u'Espa\xf1ol'],
             'spanish': [u'Italiano']},

            {'german': LanguageSwitcher().visit(german).languages,
             'french': LanguageSwitcher().visit(french).languages,
             'italian': LanguageSwitcher().visit(italian).languages,
             'spanish': LanguageSwitcher().visit(spanish).languages})

    def test_hooking_up_language_subsites_with_site_root(self):
        # Assumed that the site root is configured to be english.
        german = create(Builder('subsite').with_language('de')
                        .having(linkSiteInLanguagechooser=True))
        french = create(Builder('subsite').with_language('fr')
                        .having(linkSiteInLanguagechooser=True))

        introduce_language_subsites(german, french)

        Plone().login()

        self.assertEquals(
            # TODO: make langauges display on site root too
            {'site root': [],
             'german': [u'Fran\xe7ais', u'English'],
             'french': [u'Deutsch', u'English']},

            {'site root': LanguageSwitcher().visit_portal().languages,
             'german': LanguageSwitcher().visit(german).languages,
             'french': LanguageSwitcher().visit(french).languages})

    def test_listing_only_site_root_works(self):
        german = create(Builder('subsite').with_language('de')
                        .having(linkSiteInLanguagechooser=True))

        Plone().login().visit(german)
        self.assertEquals([u'English'], LanguageSwitcher().languages)

    def test_current_link_is_current_language(self):
        german = create(Builder('subsite').with_language('de'))
        french = create(Builder('subsite').with_language('fr'))
        introduce_language_subsites(german, french)

        Plone().login().visit(german)
        self.assertEquals(u'Deutsch', LanguageSwitcher().current)
