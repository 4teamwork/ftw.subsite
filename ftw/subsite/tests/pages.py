from ftw.testing import browser
from ftw.testing.pages import Plone


class LanguageSwitcher(Plone):

    @property
    def available(self):
        return browser().find_by_css('#portal-languageselector')

    @property
    def current(self):
        current_link = browser().find_by_css(
            '#portal-languageselector .actionMenuHeader a').first
        return current_link.text.strip()

    @property
    def language_links(self):
        return browser().find_by_css(
            '#portal-languageselector .actionMenuContent a')

    @property
    def languages(self, sort=False):
        return [link.text.strip() for link in self.language_links]

    def click_language(self, label):
        label = label.strip()
        langs = dict([(link.text.strip(), link)
                      for link in self.language_links])
        assert label in langs, \
            'Language "%s" not found in %s' % (label, langs.keys())
        langs[label].click()
        return self
