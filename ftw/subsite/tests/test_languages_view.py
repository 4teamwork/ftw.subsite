from ftw.builder import Builder
from ftw.builder import create
from ftw.subsite.tests.base import IntegrationTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles


def introduce_language_subsites(*subsites):
    for subsite in subsites:
        uids = [obj.UID() for obj in subsites]
        uids.remove(subsite.UID())
        subsite.setLanguage_references(uids)


class TestLanguagesView(IntegrationTestCase):

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_available_when_subsites_language_referenced(self):
        german = create(Builder('subsite').with_language('de'))
        french = create(Builder('subsite').with_language('fr'))
        introduce_language_subsites(german, french)
        self.assertTrue(german.restrictedTraverse('@@subsite-languages').available())

    def test_not_available_unless_languages_hooked_up(self):
        german = create(Builder('subsite').with_language('de'))
        self.assertFalse(german.restrictedTraverse('@@subsite-languages').available())

    def test_available_on_site_root_when_subsites_hooked_up(self):
        create(Builder('subsite').with_language('de')
               .having(linkSiteInLanguagechooser=True))

        self.assertTrue(
            self.portal.restrictedTraverse('@@subsite-languages').available())

    def test_not_available_on_site_root_when_not_hooked_up(self):
        self.assertFalse(
            self.portal.restrictedTraverse('@@subsite-languages').available())
