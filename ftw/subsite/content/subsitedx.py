from collective.z3cform.widgets.multicontent_search_widget import (
    MultiContentSearchFieldWidget)
from ftw.subsite import _
from ftw.subsite.interfaces import ISubsite
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Container
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import directives
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import alsoProvides
from zope.interface import implements


class ISubsiteSchema(model.Schema):
    """The Subsite schema"""

    directives.fieldset(
        'subsite',
        label=_(u'Subsite'),
        fields=('logo', 'additional_css', 'language_references',
                'link_site_in_languagechooser', 'force_language')
    )

    logo = NamedBlobImage(
        title=_(u'label_logo', default=u'Logo'),
        description=_(u'help_additional_css', default=u''),
        required=False
    )

    additional_css = schema.Text(
        title=_(u'label_additional_css', default=u'Text'),
        description=_(u'help_additional_css', default=u''),
        required=False
    )

    form.widget(language_references=MultiContentSearchFieldWidget)
    language_references = RelationList(
        title=_(u'label_language_references', default=u'Languages'),
        default=[],
        value_type=RelationChoice(title=u'Related Subsites',
                                  source=ObjPathSourceBinder(
                                      object_provides=ISubsite.__identifier__)),

        required=False,
        description=_(u'help_language_references',
                      default=_(u'The language switch will only be '
                                'displayed, if the chosen Subsite(s)'
                                'has a value in the forcelangage '
                                'field'))
    )

    link_site_in_languagechooser = schema.Bool(
        title=_(u'label_link_site_in_languagechooser',
                default=u'Link Plone Site in language chooser'),
        default=False,
        required=False)

    force_language = schema.Choice(
        title=_(u'label_forcelanguage', default=u'Subsite language'),
        description=_(u'help_forcelanguage',
                      default=u'The Subsite and it\'s content will be '
                      'delivered in the choosen language'),
        vocabulary='ftw.subsites.languages',
        required=False
    )

    from_name = schema.TextLine(
        title=_(u'label_fromname', default=u'Email Sendername'),
        description=_(u'help_fromname', default=u''),
        required=False)

    from_email = schema.TextLine(
        title=_(u'label_fromemail', default=u'Email Senderaddress'),
        description=_(u'help_fromname', default=u''),
        required=False)

alsoProvides(ISubsiteSchema, IFormFieldProvider)


class Subsite(Container):
    implements(ISubsite, INavigationRoot)
