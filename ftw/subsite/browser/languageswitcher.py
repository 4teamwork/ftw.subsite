from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter


class LanguageSwitcher(BrowserView):
    """
    changes the language by a given 'lang' parameter
    """

    def __call__(self, lang=None):

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
        httpLang = self.request.get('HTTP_ACCEPT_LANGUAGE', '')
        cookieLang = pl.getLanguageCookie()

        if lang is not None:
            prefLang = lang
        elif not lang and cookieLang:
            prefLang = cookieLang
        else:
            prefLang = httpLang[:2]

        servedLanguages = context.portal_languages.listSupportedLanguages()
        servedCodes = [l[0] for l in servedLanguages]

        if prefLang in servedCodes:
            RESPONSE.redirect(
                root_obj.aq_parent.absolute_url() + '/' + prefLang)
        else:
            RESPONSE.redirect(root_obj.aq_parent.absolute_url() + '/de')
