from zope.component import getUtility
from zope.publisher.browser import BrowserView
from plone.portlets.interfaces import IPortletManager
from plone.memoize.instance import memoize


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
