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

    def nav_root(self):
        return get_nav_root(self.context)

    def available(self):
        if ISubsite.providedBy(self.nav_root()):
            return bool(self.nav_root().getSubsite_languages())

    def languages(self):
        """Returns all possible languages based on the Subsite configuration.
        """
        ltool = getToolByName(self.nav_root(), 'portal_languages')
        languages = []
        subsites = self.nav_root().getSubsite_languages()
        if not isinstance(subsites, list):
            subsites = [subsites]
        for subsite in subsites:
            lang = subsite.getForcelanguage()
            if lang:
                languages.append(
                    dict(code=lang,
                         url=subsite.absolute_url(),
                         native=ltool.getNameForLanguageCode(lang)))
        return languages
