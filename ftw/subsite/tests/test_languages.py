from ftw.builder import Builder
from ftw.builder import create
from ftw.subsite.interfaces import ILanguages
from ftw.subsite.tests.base import IntegrationTestCase
from zope.component import getMultiAdapter


def introduce_language_subsites(*subsites):
    for subsite in subsites:
        uids = [obj.UID() for obj in subsites]
        uids.remove(subsite.UID())
        subsite.setLanguage_references(uids)


class TestLanguagesAdapterOnSubsite(IntegrationTestCase):

    def test_current_language_is_translated(self):
        german = create(Builder('subsite').with_language('de'))

        langs = getMultiAdapter((german, self.request), ILanguages)
        self.assertEquals(
            {'url': german.absolute_url(),
             'title': u'Deutsch',
             'code': 'de'},
            langs.get_current_language())

    def test_related_languages(self):
        german = create(Builder('subsite').with_language('de'))
        french = create(Builder('subsite').with_language('fr'))
        italian = create(Builder('subsite').with_language('it'))
        introduce_language_subsites(german, french, italian)

        langs = getMultiAdapter((german, self.request), ILanguages)
        self.assertEquals(
            [{'url': french.absolute_url(),
              'title': u'Fran\xe7ais',
              'code': 'fr'},

             {'url': italian.absolute_url(),
              'title': u'Italiano',
              'code': 'it'}],

            langs.get_related_languages())

    def test_related_languages_with_showing_site_root(self):
        german = create(Builder('subsite').with_language('de')
                        .having(linkSiteInLanguagechooser=True))
        french = create(Builder('subsite').with_language('fr')
                        .having(linkSiteInLanguagechooser=True))
        introduce_language_subsites(german, french)

        langs = getMultiAdapter((german, self.request), ILanguages)
        self.assertEquals(
            [{'url': self.portal.absolute_url(),
              'title': u'English',
              'code': 'en'},

             {'url': french.absolute_url(),
              'title': u'Fran\xe7ais',
              'code': 'fr'}],

            langs.get_related_languages())


class TestLanguagesAdapterOnPloneSite(IntegrationTestCase):

    def test_current_language_is_english(self):
        # The default site root language is english in the tests.
        langs = getMultiAdapter((self.portal, self.request), ILanguages)
        self.assertEquals(
            {'url': self.portal.portal_url(),
             'title': u'English',
             'code': 'en'},
            langs.get_current_language())

    def test_related_languages_lists_only_subsites_which_show_link(self):
        german = create(Builder('subsite').with_language('de')
                        .having(linkSiteInLanguagechooser=True))
        french = create(Builder('subsite').with_language('fr')
                        .having(linkSiteInLanguagechooser=True))
        create(Builder('subsite').with_language('it'))

        langs = getMultiAdapter((self.portal, self.request), ILanguages)
        self.assertEquals(
            [{'url': german.absolute_url(),
              'title': u'Deutsch',
              'code': 'de'},

             {'url': french.absolute_url(),
              'title': u'Fran\xe7ais',
              'code': 'fr'}],

            langs.get_related_languages())


class TestLanguagesAdapterOnSubsiteSubContent(IntegrationTestCase):

    def test_current_language_is_taken_from_next_parent_subsite(self):
        german = create(Builder('subsite').with_language('de'))
        folder = create(Builder('folder').within(german))

        langs = getMultiAdapter((folder, self.request), ILanguages)
        self.assertEquals(
            {'url': german.absolute_url(),
             'title': u'Deutsch',
             'code': 'de'},
            langs.get_current_language())

    def test_current_language_is_taken_from_parent_site_root(self):
        folder = create(Builder('folder'))

        langs = getMultiAdapter((folder, self.request), ILanguages)
        self.assertEquals(
            {'url': self.portal.portal_url(),
             'title': u'English',
             'code': 'en'},
            langs.get_current_language())

    def test_related_languages_is_inherited_from_parent_subsite(self):
        german = create(Builder('subsite').with_language('de')
                        .having(linkSiteInLanguagechooser=True))
        french = create(Builder('subsite').with_language('fr')
                        .having(linkSiteInLanguagechooser=True))
        introduce_language_subsites(german, french)

        folder = create(Builder('folder').within(german))

        langs = getMultiAdapter((folder, self.request), ILanguages)
        self.assertEquals(
            [{'url': self.portal.absolute_url(),
              'title': u'English',
              'code': 'en'},

             {'url': french.absolute_url(),
              'title': u'Fran\xe7ais',
              'code': 'fr'}],

            langs.get_related_languages())

    def test_related_languages_is_inherited_from_site_root(self):
        german = create(Builder('subsite').with_language('de')
                        .having(linkSiteInLanguagechooser=True))
        french = create(Builder('subsite').with_language('fr')
                        .having(linkSiteInLanguagechooser=True))

        folder = create(Builder('folder'))

        langs = getMultiAdapter((folder, self.request), ILanguages)
        self.assertEquals(
            [{'url': german.absolute_url(),
              'title': u'Deutsch',
              'code': 'de'},

             {'url': french.absolute_url(),
              'title': u'Fran\xe7ais',
              'code': 'fr'}],

            langs.get_related_languages())
