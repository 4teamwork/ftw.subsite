from Acquisition import aq_inner, aq_parent
from Products.CMFPlone.interfaces import IPloneSiteRoot
from ftw.subsite.interfaces import ISubsite
from plone import api
from plone.app.layout.analytics.view import AnalyticsViewlet


class SubsiteAnalyticsViewlet(AnalyticsViewlet):
    def update(self):
        self.csutom_analytics_snippet = self.get_custom_analytics_snippet()

    def render(self):
        default_snippet = super(SubsiteAnalyticsViewlet, self).render()
        return self.csutom_analytics_snippet or default_snippet

    def get_custom_analytics_snippet(self):
        obj = self.context
        while not IPloneSiteRoot.providedBy(obj):

            if ISubsite.providedBy(obj):
                snippet = obj.getWebstatsAnalyticsSnippet()
                if snippet:
                    return snippet

            # Get the parent of the current obj (which is not a subsite if
            # we are down here) because the navigation root of a navigation
            # root is the obj itself.
            obj = aq_parent(aq_inner(obj))
            obj = api.portal.get_navigation_root(context=obj)

        return None
