from plone.app.layout.viewlets.common import LogoViewlet
from plone.app.layout.navigation.root import getNavigationRoot
from borg.localrole.interfaces import IFactoryTempFolder
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.interfaces._content import IContentish


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

        subsite_logo = getattr(self.context, 'getLogo', None)
        parent = self.context.aq_inner.aq_parent
        in_factory = IFactoryTempFolder.providedBy(parent)

        if subsite_logo and subsite_logo() and not in_factory:
            # we are in a subsite
            context = self.context
            if not IContentish.providedBy(context):
                context = context.aq_parent
            navigation_root_path = getNavigationRoot(context)
            scale = portal.restrictedTraverse(
                navigation_root_path + '/@@images')
            # XXX Use own scale
            self.logo_tag = scale.scale('logo', scale="logo").tag()
            self.title = self.context.restrictedTraverse(
                getNavigationRoot(self.context)).Title()
            self.is_subsitelogo = True
        else:
            # standard plone logo
            logoName = portal.restrictedTraverse('base_properties').logoName
            self.logo_tag = portal.restrictedTraverse(logoName).tag()
            self.title = self.portal_state.portal_title()
