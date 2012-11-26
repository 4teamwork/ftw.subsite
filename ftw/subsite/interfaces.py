from zope.interface import Interface
from plone.app.portlets.interfaces import IColumn


class ISubsite(Interface):
    """
    marker interface for subsite content type
    """


class ISubsiteColumn(IColumn):
    """
    Marker Inerface for front view columns
    """


class IFtwSubsiteLayer(Interface):
    """
    Browserlayer
    """
