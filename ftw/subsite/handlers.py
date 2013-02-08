from ftw.subsite.interfaces import ISubsite
from ftw.subsite.utils import find_context
from ftw.subsite.utils import get_nav_root
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletManager
from zope.component import adapter
from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import ComponentLookupError
from ZPublisher.interfaces import IPubAfterTraversal
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import IFolderish


def block_parent_portlets(object_, event):
    """Block parent portlets for Subsite columns
    """
    if 'portal_factory' in object_.getPhysicalPath():
        # do not run in portal_factory
        pass
    else:
        for i in range(1, 7):
            # We have 6 column manager on subsites
            try:
                manager = getUtility(IPortletManager,
                                     name='ftw.subsite.front%s' % str(i))

            except ComponentLookupError:
                # This happens when the plone site is removed.
                # In this case persistent utilites are already gone.
                # Reindexing is not necessary in this situation, since
                # everything will be gone.
                return

            assignable = getMultiAdapter((object_, manager,),
                                         ILocalPortletAssignmentManager)
            assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)


@adapter(IPubAfterTraversal)
def language_negotiator(event):

    # Get current published object
    obj = find_context(event.request)

    # Filter out CSS/JS and other non contentish objects
    # IFolderish check includes site root
    if not (IContentish.providedBy(obj) or IFolderish.providedBy(obj)):
        return None

    nav_root = get_nav_root(obj)

    if ISubsite.providedBy(nav_root):
        # Get language stored on Subsite
        language = nav_root.Schema().get('forcelanguage').get(nav_root)
        if language:
            event.request['LANGUAGE'] = language
            event.request.LANGUAGE_TOOL.LANGUAGE = language
