from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def uninstall_plone5(portal):
    clean_plone5_registry(portal)


def clean_plone5_registry(portal):
    registry = getUtility(IRegistry)

    allowed_sizes = registry['plone.allowed_sizes']
    allowed_sizes.remove(u'bannerimage 960:130')
    allowed_sizes.remove(u'logo 215:56')
    registry['plone.allowed_sizes'] = allowed_sizes

    displayed_types = list(registry['plone.displayed_types'])
    displayed_types.remove(u'ftw.subsite.Subsite')
    registry['plone.displayed_types'] = tuple(displayed_types)
