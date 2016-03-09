from ftw.subsite.tests.interfaces import IExampleDxType
from plone.dexterity.content import Item
from zope.interface import implements


class ExampleDxType(Item):
    implements(IExampleDxType)
