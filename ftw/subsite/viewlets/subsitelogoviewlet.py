from plone.app.layout.viewlets.common import LogoViewlet
from plone.app.layout.navigation.root import getNavigationRoot
from borg.localrole.interfaces import IFactoryTempFolder
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SubsiteLogoViewlet(LogoViewlet):
    index = ViewPageTemplateFile('subsitelogoviewlet.pt')

    def __init__(self, context, request, view, manager=None):
        super(SubsiteLogoViewlet, self).__init__(
            context, request, view, manager)
        self.navigation_root_url = None
        self.logo_tag = None
        self.title = None

    def update(self):
        super(SubsiteLogoViewlet, self).update()

        portal = self.portal_state.portal()
        self.navigation_root_url = self.portal_state.navigation_root_url()

        subsite_logo = getattr(self.context, 'getLogo', None)
        in_factory = IFactoryTempFolder.providedBy(
            self.context.aq_inner.aq_parent)

        if subsite_logo and len(subsite_logo()) and not in_factory:
            # we are in a subsite
            navigation_root_path = self.portal_state.navigation_root_path()
            scale = portal.restrictedTraverse(
                navigation_root_path + '/@@images')
            # XXX Use own scale
            self.logo_tag = scale.scale('logo', scale="mini").tag()
            self.title = self.context.restrictedTraverse(
                getNavigationRoot(self.context)).Title()
        else:
            # standard plone logo
            logoName = portal.restrictedTraverse('base_properties').logoName
            self.logo_tag = portal.restrictedTraverse(logoName).tag()
            self.title = self.portal_state.portal_title()
