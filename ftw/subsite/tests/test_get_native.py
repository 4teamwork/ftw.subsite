import unittest2 as unittest
from ftw.subsite.testing import FTW_SUBSITE_INTEGRATION_TESTING
from ftw.subsite.browser.selector import LanguageSelector


class TestGetLanguageNative(unittest.TestCase):

    layer = FTW_SUBSITE_INTEGRATION_TESTING

    def setUp(self):
        self.selector = LanguageSelector(object(), object(), object())
        self.ltool = self.layer['portal'].portal_languages

    def test_return_native_for_existing_language(self):
        """Test If our function returns the correct Native, if the Language exists"""
        native = self.selector.getNativeForLanguageCode(self.ltool, 'sv')
        self.assertEqual(u'Svenska', native)

    def test_returns_none_for_invalid_language(self):
        """Check if function returns nothing when the language doesn't exist.'"""
        native = self.selector.getNativeForLanguageCode(self.ltool, 'hans')
        self.assertEqual(None, native)
