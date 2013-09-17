from ftw.testing import browser
from ftw.testing.pages import Plone


class LanguageSwitcher(Plone):

    @property
    def available(self):
        return browser().find_by_css('#portal-languageselector')

    @property
    def languages(self, sort=False):
        links = browser().find_by_css('#portal-languageselector a')
        return [link.text.strip() for link in links]

    def click_language(self, label):
        label = label.strip()
        links = browser().find_by_css('#portal-languageselector a')
        langs = dict([(link.text.strip(), link) for link in links])
        assert label in langs, \
            'Language "%s" not found in %s' % (label, langs.keys())
        langs[label].click()
        return self
