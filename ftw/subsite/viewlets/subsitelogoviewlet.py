from Products.CMFCore.interfaces._content import IContentish
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.viewlets.common import LogoViewlet
import pkg_resources

IS_PLONE_5 = pkg_resources.get_distribution('Products.CMFPlone').version >= '5'


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

        navroot = api.portal.get_navigation_root(self.context)
        is_subsite = bool(navroot.portal_type == 'ftw.subsite.Subsite')

        self.navigation_root_url = self.portal_state.navigation_root_url()

        subsite_logo = getattr(navroot, 'logo', None)
        subsite_logo_alt_text = getattr(navroot, 'logo_alt_text', None)

        if is_subsite and subsite_logo and subsite_logo.data:
            # we are in a subsite
            context = self.context
            if not IContentish.providedBy(context):
                context = context.aq_parent
            navigation_root_path = getNavigationRoot(context)
            scale = navroot.restrictedTraverse(
                navigation_root_path + '/@@images')

            self.logo_tag = scale.scale('logo', scale="logo").tag(
                alt=subsite_logo_alt_text, title=None)
            self.title = self.context.restrictedTraverse(
                getNavigationRoot(self.context)).Title()
            self.is_subsitelogo = True
        else:
            # standard plone logo
            if not IS_PLONE_5:
                portal = api.portal.get()
                logoName = navroot.restrictedTraverse('base_properties').logoName
                logo_alt_text = portal.getProperty('logo_alt_text', '')
                self.logo_tag = portal.restrictedTraverse(logoName).tag(
                    alt=logo_alt_text, title='')
                self.title = self.portal_state.portal_title()

            if IS_PLONE_5:
                portal = api.portal.get()
                self.title = self.portal_state.portal_title()
                rel_context_path = "/".join(self.context.getPhysicalPath())
                logo_path = '{}/logo.png'.format(rel_context_path)
                self.logo_tag = portal.restrictedTraverse(logo_path).tag(
                    alt=self.title, title='')
                self.is_subsitelogo = False
