from ftw.builder import Builder
from ftw.builder import create
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from unittest2 import TestCase


class TestSubsite(TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        self.subsite = create(Builder('subsite')
                              .titled(u'Subsute')
                              .having(additional_css='p {color: red;}'))

        self.styles = '<style type="text/css" media="all">p {color: red;}</style>'

    @browsing
    def test_cssviewlet_in_subsite(self, browser):
        browser.login().visit(self.subsite)

        self.assertIn(self.styles,
                      browser.contents,
                      'Did not found the substes styles.')
        browser.visit(self.portal)
        self.assertNotIn(self.styles,
                         browser.contents,
                         'Found unexpeted subsite styles.')

    @browsing
    def test_cssviewlet_in_subfolder(self, browser):
        folder = create(Builder('folder').within(self.subsite))
        browser.login().visit(folder)
        self.assertIn(self.styles,
                      browser.contents,
                      'Did not found the substes styles.')
