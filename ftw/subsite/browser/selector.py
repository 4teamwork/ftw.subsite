from zope.interface import implements
from zope.viewlet.interfaces import IViewlet
from ftw.subsite.interfaces import ISubsite
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class LanguageSelector(BrowserView):
    """Language selector.
    """
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(LanguageSelector, self).__init__(context, request)
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.nav_root = None

    def available(self):
        plone_state = self.context.restrictedTraverse('@@plone_portal_state')
        navigation_root_path = plone_state.navigation_root_path()
        self.nav_root = self.context.restrictedTraverse(navigation_root_path)
        return ISubsite.providedBy(self.nav_root)

    def languages(self):
        """Returns list of languages."""
        languages = self.nav_root.getSubsite_languages()
        lang_dicts = []
        lang_tool = getToolByName(self.nav_root, 'portal_languages')
        for language in languages:
            lang_dicts.append(
                {'code': language,
                 'native': lang_tool.getNameForLanguageCode(language)})
        return lang_dicts
