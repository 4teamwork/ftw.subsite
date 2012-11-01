from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.navigation.root import getNavigationRoot
from borg.localrole.interfaces import IFactoryTempFolder
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class SubsiteLogoViewlet(ViewletBase):
    index = ViewPageTemplateFile('subsitelogoviewlet.pt')

    def update(self):
        super(SubsiteLogoViewlet, self).update()
        portal = self.portal_state.portal()
        self.navigation_root_url = self.portal_state.navigation_root_url()
        subsite_logo = getattr(self.context, 'logo', None)
        if subsite_logo and not IFactoryTempFolder.providedBy(self.context): # we are in a subsite
            scale = portal.restrictedTraverse('/'.join(self.context.getPhysicalPath())+'/@@images')
            self.logo_tag = scale.scale('logo', scale="mini").tag()
            self.portal_title = self.context.restrictedTraverse(getNavigationRoot(self.context)).title
        else: # standard plone logo
            logoName = portal.restrictedTraverse('base_properties').logoName
            self.logo_tag = portal.restrictedTraverse(logoName).tag()
            self.portal_title = self.portal_state.portal_title() 
