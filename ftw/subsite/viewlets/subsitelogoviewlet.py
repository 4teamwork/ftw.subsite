from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.viewlets.common import LogoViewlet
from Products.CMFCore.interfaces._content import IContentish
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SubsiteLogoViewlet(LogoViewlet):
    index = ViewPageTemplateFile('subsitelogoviewlet.pt')

    def __init__(self, context, request, view, manager=None):
        super(SubsiteLogoViewlet, self).__init__(
            context, request, view, manager)
        self.navigation_root_url = None
        self.logo_tag = None
        self.title = None
        self.is_subsitelogo = False

    def update(self):
        super(SubsiteLogoViewlet, self).update()

        portal = self.portal_state.portal()
        self.navigation_root_url = self.portal_state.navigation_root_url()

        subsite_logo = getattr(self.context, 'logo', None)
        subsite_logo_alt_text = getattr(self.context, 'logo_alt_text', None)

        if subsite_logo and subsite_logo.data:
            # we are in a subsite
            context = self.context
            if not IContentish.providedBy(context):
                context = context.aq_parent
            navigation_root_path = getNavigationRoot(context)
            scale = portal.restrictedTraverse(
                navigation_root_path + '/@@images')

            self.logo_tag = scale.scale('logo', scale="logo").tag(
                alt=subsite_logo_alt_text, title=None)
            self.title = self.context.restrictedTraverse(
                getNavigationRoot(self.context)).Title()
            self.is_subsitelogo = True
        else:
            # standard plone logo
            logoName = portal.restrictedTraverse('base_properties').logoName
            logo_alt_text = portal.getProperty('logo_alt_text', '')
            self.logo_tag = portal.restrictedTraverse(logoName).tag(
                alt=logo_alt_text, title='')
            self.title = self.portal_state.portal_title()
