from Products.CMFCore.utils import getToolByName
from ftw.builder import Builder
from ftw.builder import create
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase
import transaction


class TestAnalytics(TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])
        login(self.portal, TEST_USER_NAME)

        proprties_tool = getToolByName(self.portal, 'portal_properties')
        proprties_tool.site_properties.webstats_js = '<script foo="bar">Default Analytics Snippet</script>'
        transaction.commit()

    @browsing
    def test_plone_site_renders_default_analytics(self, browser):
        """
        This test makes sure that the plone site renders the default
        analytics snippet.
        """
        browser.login().visit(self.portal)
        self.assertEqual(
            'Default Analytics Snippet',
            browser.css('script[foo="bar"]').first.text
        )

    @browsing
    def test_content_renders_default_analytics(self, browser):
        """
        This test makes sure that the content renders the default
        analytics snippet.
        """
        folder = create(Builder('folder').within(self.portal))
        browser.login().visit(folder)
        self.assertEqual(
            'Default Analytics Snippet',
            browser.css('script[foo="bar"]').first.text
        )

    @browsing
    def test_subsite_without_custom_analytics(self, browser):
        """
        This test makes sure that a subsite not having a custom
        analytics snippet renders the default analytics snippet.
        """
        subsite = create(Builder('subsite').within(self.portal))
        browser.login().visit(subsite)
        self.assertEqual(
            'Default Analytics Snippet',
            browser.css('script[foo="bar"]').first.text
        )

    @browsing
    def test_subsite_with_custom_analytics(self, browser):
        """
        This test makes sure that a subsite having a custom analytics
        snippet renders the custom analytics snippet instead of the default
        analytics snippet.
        """
        subsite = create(Builder('subsite')
                         .within(self.portal)
                         .having(webstatsAnalyticsSnippet='<script foo="bar">Custom Analytics Snippet</script>'))
        browser.login().visit(subsite)
        self.assertEqual(
            'Custom Analytics Snippet',
            browser.css('script[foo="bar"]').first.text
        )

    @browsing
    def test_content_within_subsite_with_custom_analytics(self, browser):
        """
        This test makes sure that content within a subsite having
        a custom analytics snippet also renders the custom analytics snippet.
        """
        subsite = create(Builder('subsite')
                         .within(self.portal)
                         .having(webstatsAnalyticsSnippet='<script foo="bar">Custom Analytics Snippet</script>'))
        folder = create(Builder('folder').within(subsite))
        browser.login().visit(folder)
        self.assertEqual(
            'Custom Analytics Snippet',
            browser.css('script[foo="bar"]').first.text
        )
