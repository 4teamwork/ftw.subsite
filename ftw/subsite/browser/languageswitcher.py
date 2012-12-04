from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter


class LanguageSwitcher(BrowserView):
    """
    changes the language by a given 'lang' parameter
    """

    def __call__(self):
        query_string = self.request.get('QUERY_STRING')
        param, lang = query_string.split('=')
        if not param == "set_language":
            return self.request.RESPONSE.redirect(self.context.absolute_url())
        context = self.context
        RESPONSE = self.request.RESPONSE
        pl = context.portal_languages
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')

        root_obj = context.restrictedTraverse(
            portal_state.navigation_root_path())

        if lang:
            pl.setLanguageCookie(lang)

        prefLang = pl.getPreferredLanguage()
        cookieLang = pl.getLanguageCookie()
        if lang is not '':
            prefLang = lang
        else:
            prefLang = cookieLang

        try:
            obj = root_obj.restrictedTraverse(
                '/'.join(root_obj.aq_parent.getPhysicalPath()) + '/' + prefLang)
        except KeyError:
            return RESPONSE.redirect(context.absolute_url())
        return RESPONSE.redirect(obj.absolute_url())
