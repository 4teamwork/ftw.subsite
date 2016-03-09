from Acquisition._Acquisition import aq_inner
from Acquisition._Acquisition import aq_parent
from Products.CMFPlone.interfaces import IPloneSiteRoot
from ftw.subsite.interfaces import ISubsite
from plone import api
from plone.app.layout.viewlets.common import LogoViewlet
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
        portal = api.portal.get()
        subsite = self.get_nearest_subsite_with_logo()
        if subsite:
            subsite_image_scales_path = '/'.join(
                list(subsite.getPhysicalPath()) + ['@@images']
            )
            scales = portal.restrictedTraverse(subsite_image_scales_path)
            self.logo_tag = scales.scale('logo', scale="logo").tag()
            self.title = subsite.Title()
            self.is_subsitelogo = True
        else:
            # standard plone logo
            logoName = portal.restrictedTraverse('base_properties').logoName
            self.logo_tag = portal.restrictedTraverse(logoName).tag()
            self.title = self.portal_state.portal_title()

    def get_nearest_subsite_with_logo(self):
        obj = self.context
        while obj and not IPloneSiteRoot.providedBy(obj):

            if ISubsite.providedBy(obj):
                if obj.Schema()['logo'].get_size(obj):
                    return obj

            # Get the parent of the current obj (which is not a subsite if
            # we are down here) because the navigation root of a navigation
            # root is the obj itself.
            obj = aq_parent(aq_inner(obj))
            if obj:
                obj = api.portal.get_navigation_root(context=obj)

        return None
