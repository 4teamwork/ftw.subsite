from ftw.subsite.migration.subsite_migration import subsite_migrator
from plone.app.contenttypes.migration.browser import pass_fn
from plone.app.contenttypes.migration.browser import PATCH_NOTIFY
from plone.app.contenttypes.migration.patches import patched_insertForwardIndexEntry
from Products.contentmigration.utils import patch
from Products.contentmigration.utils import undoPatch
from Products.PluginIndexes.UUIDIndex.UUIDIndex import UUIDIndex
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from Products.CMFCore.utils import getToolByName
from plone.app.uuid.utils import uuidToObject


def restore_language_references(portal):
    catalog = getToolByName(portal, "portal_catalog")
    for brain in catalog(portal_type='ftw.subsite.Subsite'):
        subsite = brain.getObject()
        if hasattr(subsite, '_language_reference_uids'):
            intids = getUtility(IIntIds)
            relations = []
            for uid in subsite._language_reference_uids:
                referenced_subsite = uuidToObject(uid)
                if referenced_subsite is None:
                    return
                else:
                    relations.append(RelationValue(
                        intids.getId(referenced_subsite)))
            subsite.language_references = relations


class SubsiteMigration(object):

    portal = None

    def __init__(self, portal):
        self.portal = portal

    def __call__(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        self.patch_notify_modified()
        patch(
            UUIDIndex,
            'insertForwardIndexEntry',
            patched_insertForwardIndexEntry)

        subsite_migrator(self.portal)

        catalog.clearFindAndRebuild()

        restore_language_references(self.portal)

    def patch_notify_modified(self):
        """Patch notifyModified to prevent setModificationDate() on changes

        notifyModified lives in several places and is also used on folders
        when their content changes.
        So when we migrate Documents before Folders the folders
        ModifiedDate gets changed.
        """
        for klass in PATCH_NOTIFY:
            patch(klass, 'notifyModified', pass_fn)

    def reset_notify_modified(self):
        """reset notifyModified to old state"""
        for klass in PATCH_NOTIFY:
            undoPatch(klass, 'notifyModified')
