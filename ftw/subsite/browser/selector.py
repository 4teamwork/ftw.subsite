from zope.interface import implements
from zope.viewlet.interfaces import IViewlet
from ftw.subsite.interfaces import ISubsite
from Products.CMFCore.utils import getToolByName
from ftw.subsite.utils import get_nav_root
from plone.app.layout.viewlets import common


class LanguageSelector(common.ViewletBase):
    """Language selector.
    """
    implements(IViewlet)

    def __init__(self, *args, **kwargs):
        super(LanguageSelector, self).__init__(*args, **kwargs)
        self._nav_root = None

    @property
    def navigation_root(self):
        if self._nav_root is None:
            self._nav_root = get_nav_root(self.context)
        return self._nav_root

    def available(self):
        if not ISubsite.providedBy(self.navigation_root):
            return False

        elif self.navigation_root.showLinkToSiteInLanguageChooser():
            return True

        else:
            return bool(self.navigation_root.getLanguage_references())

    def current(self):
        ltool = getToolByName(self.navigation_root, 'portal_languages')
        return self.getNativeForLanguageCode(
            ltool, self.navigation_root.getForcelanguage())

    def languages(self):
        """Returns all possible languages based on the Subsite configuration.
        """
        ltool = getToolByName(self.navigation_root, 'portal_languages')
        languages = []
        subsites = self.navigation_root.getLanguage_references()

        for subsite in subsites:
            lang = subsite.getForcelanguage()
            if lang:
                languages.append(
                    dict(code=lang,
                         url=subsite.absolute_url(),
                         native=self.getNativeForLanguageCode(ltool, lang)))

        if self.navigation_root.showLinkToSiteInLanguageChooser():
            portal_url = getToolByName(self.navigation_root, 'portal_url')
            lang = ltool.getDefaultLanguage()

            languages.append(
                dict(code=lang,
                     url=portal_url(),
                     native=self.getNativeForLanguageCode(ltool, lang)))

        return languages

    def getNativeForLanguageCode(self, ltool, langCode):
        """Returns the name for a language code."""
        info = ltool.getAvailableLanguageInformation().get(langCode, None)
        if info is not None:
            return info.get(u'native', None)
        return None
