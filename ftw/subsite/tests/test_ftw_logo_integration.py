from ftw.builder import Builder
from ftw.builder import create
from ftw.subsite.browser.subsiteview import SubsiteView
from ftw.subsite.interfaces import IFtwSubsiteLayer
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobImage
from unittest2 import TestCase
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager
import os
import transaction
from Products.CMFCore.utils import getToolByName


class TestFtwLogoIntegration(TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.subsite = create(Builder('subsite').titled(u'MySubsite'))

    @browsing
    def test_logo_view(self, browser):
        browser.login()
        browser.open(self.portal, view='logo-and-icon-overrides')
        # I assert the title because I assume that if the title
        # is loaded we successfully loaded the page
        self.assertEqual('Manually set site Logos and Icons',
                         browser.css('h1').first.text,
                         'The pages title should be different')
