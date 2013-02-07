"""Definition of the OrgUnit content type
"""

from ftw.subsite import _
from ftw.subsite.config import PROJECTNAME
from ftw.subsite.interfaces import ISubsite
from plone.app.blob.field import ImageField
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName
from zope.interface import implements


schema = atapi.Schema((
    ImageField(
        name='logo',
        required=False,
        storage=atapi.AnnotationStorage(),
        schemata='subsite',
        widget=atapi.ImageWidget(
            label=_(u'label_logo',
                    default=u'Logo'),
            description=_(u'help_logo',
                          default=u''))),

    atapi.TextField(
            name='additional_css',
            storage=atapi.AnnotationStorage(),
            schemata='subsite',
            widget=atapi.TextAreaWidget(
                rows=15,
                label=_(u'label_additional_css',
                        default=u'Additional CSS'),
                description=_(u'help_additional_css',
                              default=u''))),

    atapi.LinesField(
        name='subsite_languages',
        storage=atapi.AnnotationStorage(),
        schemata='subsite',
        widget=atapi.LinesWidget(
            label=_(u'label_subsite_languages',
                    default=u'Languages'),
            description=_(u'_helpsubsite_languages',
                          default=u'add one language per line, ex. "de", "en",'
                                   'etc. be sure the subsites have the same '
                                   'ids (de, en, etc.), all subsite with a '
                                   'specifig language must be siblings'))),

    atapi.StringField(
        name="forcelanguage",
        vocabulary_factory="plone.app.vocabularies.AvailableContentLanguages",
        widget=atapi.SelectionWidget(
            label=_(u'label_forcelanguage', default=u'Subsite language'),
            description=_(u'help_forcelanguage',
                          default=u'The Subsite and it\'s content will be '
                                   'delivered in the choosen language'))),

    atapi.StringField(
        name="FromName",
        widget=atapi.StringWidget(
            label=_(u'label_fromname', default=u'Email Sendername'),
            description=_(u'help_fromname', default=u''))),

    atapi.StringField(
        name="FromEmail",
        widget=atapi.StringWidget(
            label=_(u'label_fromemail', default=u'Email Senderaddress'),
            description=_(u'help_fromname', default=u'')))
))


subsite_schema = folder.ATFolder.schema.copy() + schema

schemata.finalizeATCTSchema(
    subsite_schema,
    folderish=True,
    moveDiscussion=False,
    )


class Subsite(folder.ATFolder):
    """Subsite Unit"""
    implements(ISubsite, INavigationRoot)

    schema = subsite_schema
    meta_type = "Subsite"

atapi.registerType(Subsite, PROJECTNAME)
