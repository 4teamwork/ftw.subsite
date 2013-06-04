from ftw.subsite.browser.sitemap import SubsiteSitemapQueryBuilder
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from pyquery import PyQuery
import transaction
import unittest2


class TestSubsiteSitemap(unittest2.TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestSubsiteSitemap, self).setUp()
        self.portal = self.layer['portal']

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

        self.subsite = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'mysubsite',
            title="My Subsite"))

        self.folder = self.subsite.get(
            self.subsite.invokeFactory('Folder', 'folder',
                                       title="Folder"))

        transaction.commit()

    def test_subsite_query_builder_on_plone_root(self):
        query = SubsiteSitemapQueryBuilder(self.portal)()

        self.assertEquals(query['path']['query'], '/plone',
            'Expect portal root')

    def test_subsite_query_builder_on_subsite(self):
        query = SubsiteSitemapQueryBuilder(self.subsite)()

        self.assertEquals(query['path']['query'], '/plone/mysubsite',
            'Expect subsite path')

    def test_subsite_query_builder_on_folder_in_subsite(self):
        query = SubsiteSitemapQueryBuilder(self.folder)()

        self.assertEquals(query['path']['query'], '/plone/mysubsite',
            'Expect subsite path, because the folder is in a subsite')

    def test_subsite_sitemap_view_on_plone_root(self):
        self.browser.open("%s/sitemap" % self.portal.absolute_url())
        doc = PyQuery(self.browser.contents)
        subsite = doc('#content-core a[href="http://nohost/plone/mysubsite"]')

        self.assertEquals(len(subsite), 1, 'Expect to find our Subsite')

    def test_subsite_sitemap_view_on_subsite_root(self):
        self.browser.open("%s/sitemap" % self.subsite.absolute_url())
        doc = PyQuery(self.browser.contents)
        subsite = doc('#content-core a[href="http://nohost/plone/mysubsite"]')

        self.assertEquals(len(subsite), 0, 'There should be no subsite')

        folder = doc(
            '#content-core a[href="http://nohost/plone/mysubsite/folder"]')
        self.assertEquals(len(folder), 1, 'Expect one folder')
