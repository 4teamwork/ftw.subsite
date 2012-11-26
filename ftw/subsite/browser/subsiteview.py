from zope.component import getUtility
from zope.publisher.browser import BrowserView
from plone.portlets.interfaces import IPortletManager
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from ftw.subsite.interfaces import ISubsite


class SubsiteView(BrowserView):

    @memoize
    def empty(self):
        dashboards = [getUtility(IPortletManager, name=name) for name in
                        ['ftw.subsite.front1',
                         'ftw.subsite.front2',
                         'ftw.subsite.front3',
                         'ftw.subsite.front4',
                         'ftw.subsite.front5',
                         'ftw.subsite.front6']]

        num_portlets = 0
        for dashboard in dashboards:
            num_portlets += len(dashboard)
        return num_portlets == 0

    def hasPermissions(self):
        member_tool = getToolByName(self, 'portal_membership')
        current_context = self.context
        permissionToCheck = 'Review portal content'

        isAnon = member_tool.isAnonymousUser()

        if not isAnon:
            hasPermission = member_tool.getAuthenticatedMember().has_permission(
                permissionToCheck, current_context)
        else:
            return False

        if hasPermission:
            return True
        else:
            return False

    def is_subsite(self):
        return ISubsite.proviedBy(self.context.aq_explicit)
