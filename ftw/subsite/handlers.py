from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletManager
from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import ComponentLookupError

def remove_parent_portlets(object_, event):
    """Adds a custom navigation Portlet for Buch
    """
    if 'portal_factory' in object_.getPhysicalPath():
        # do not run in portal_factory
        pass
    else:
        for i in range(1, 7):
            try:
                manager = getUtility(IPortletManager, name='ftw.subsite.front%s' % str(i))

            except ComponentLookupError:
                # This happens when the plone site is removed.
                # In this case persistent utilites are already gone.
                # Reindexing is not necessary in this situation, since
                # everything will be gone.
                return

            assignable = getMultiAdapter((object_, manager,),
                                         ILocalPortletAssignmentManager)
            assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)
