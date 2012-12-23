from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize import instance
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.navigation.root import getNavigationRoot
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from random import choice


class Banner(common.ViewletBase):
    render = ViewPageTemplateFile('banner_viewlet.pt')

    @property
    def available(self):
        return bool(self.get_banners())

    @instance.memoize
    def get_banners(self):
        bannerfolder = self.get_banner_folder()
        if not bannerfolder:
            return []

        registry = getUtility(IRegistry)
        root_only = registry.get('ftw.subsite.banner_root_only', True)

        query = dict(portal_type='Image')
        imgs = bannerfolder.getFolderContents(contentFilter=query,
                                              full_objects=True)

        if root_only:
            context_state = self.context.restrictedTraverse(
                '@@plone_context_state')
            nav_root = INavigationRoot.providedBy(self.context)
            if context_state.is_portal_root() or nav_root:
                return imgs
            return []
        else:
            return imgs

    def get_banner_folder(self):
        registry = getUtility(IRegistry)
        nav_context = self.context.restrictedTraverse(
            getNavigationRoot(self.context)).aq_explicit

        name = registry.get('ftw.subsite.bannerfoldername', 'banners')
        bannerfolder = getattr(nav_context, name, None)
        return bannerfolder

    def get_banner_tag(self):
        title = self.context.title_or_id()
        img = choice(self.get_banners())
        scales = img.restrictedTraverse('@@images')
        return scales.tag('image', scale='bannerimage', alt=title,
                            title=title)
