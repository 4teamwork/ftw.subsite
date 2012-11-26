"""Definition of the OrgUnit content type
"""

from Products.Archetypes import atapi
from ftw.subsite import _
from ftw.subsite.config import PROJECTNAME
from ftw.subsite.interfaces import ISubsite
from zope.interface import implements
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from plone.app.blob.field import ImageField

schema = atapi.Schema((

        ImageField(
            name='logo',
            required=True,
            storage=atapi.AnnotationStorage(),
            schemata='subsite',
            widget=atapi.ImageWidget(
                label=_(u'label_logo',
                        default=u'Logo'),
                description=_(u'help_logo',
                              default=u''),
                ),
            ),


        atapi.TextField(
                name='additional_css',
                storage=atapi.AnnotationStorage(),
                schemata='subsite',
                widget=atapi.TextAreaWidget(
                    rows=15,
                    label=_(u'label_additional_css',
                            default=u'Additional CSS'),
                    description=_(u'help_additional_css',
                                  default=u''),
                    ),
                ),


            atapi.LinesField(
                name='subsite_languages',
                storage=atapi.AnnotationStorage(),
                schemata='subsite',
                widget=atapi.LinesWidget(
                    label=_(u'label_subsite_languages',
                            default=u'Languages'),
                    description=_(u'_helpsubsite_languages',
                                  default=u'add one language per line, \
 ex. "de", "en", etc. be sure the subsites have the same ids (de, en, etc.), \
 all subsite with a specifig language must be siblings'),
                    ),
                ),
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

    logo = atapi.ATFieldProperty('logo')
    additional_css = atapi.ATFieldProperty('additional_css')
    tabs = atapi.ATFieldProperty('tabs')
    zug_languages = atapi.ATFieldProperty('subsite_languages')

    def get_possible_tabs(self):
        """
        simply returns the folder contents
        """
        results = []
        #append spacer

        results.append(('spacer', 'spacer'))
        for item in self.getFolderContents(
            contentFilter={'is_folderish': True}):
            results.append((item.id, item.id))
        return (atapi.DisplayList(results))


atapi.registerType(Subsite, PROJECTNAME)
