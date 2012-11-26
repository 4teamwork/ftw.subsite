from zope.interface import implements
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from zope import schema
from z3c.form import form, button, field
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from plone.formwidget.contenttree import PathSourceBinder
from plone.formwidget.contenttree import ContentTreeFieldWidget
from plone.app.z3cform.wysiwyg.widget import WysiwygFieldWidget
from z3c.form.interfaces import INPUT_MODE
from plone.namedfile.field import NamedImage
from Acquisition import aq_inner, aq_parent


class ITeaserPortlet(IPortletDataProvider):
    """A portlet which can some given Infos
    """

    teasertitle = schema.TextLine(title=_(u'Teaser Titel'),
                                  description=_(u'Geben Sie einen Titel ein'),
                                  required=True)

    teaserdesc = schema.Text(title=_(u'Teaser Beschreibung'),
                             description=_(u"Geben Sie einen Beschrieb ein."),
                             required=True)

    internal_target = schema.Choice(title=_(u"Internal Target"),
                                    description=_(u"Find an internal target \
 for this image to link to"),
                                   required=True,
                                   source=PathSourceBinder({})
                                    )
    image = NamedImage(title=u'Image field',
                        description=u"Add or replace image for the portlet",
                        required=True)


class Assignment(base.Assignment):
    implements(ITeaserPortlet)

    def __init__(self, assignment_context_path=None, teasertitle='',
                 teaserdesc='', image=None, internal_target=None):
        self.assignment_context_path = assignment_context_path
        self.teasertitle = teasertitle
        self.teaserdesc = teaserdesc
        self.image = image
        self.internal_target = internal_target

    @property
    def title(self):
        if self.teasertitle:
            return self.teasertitle
        else:
            return 'Teaserportlet'


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('teaserportlet.pt')

    def getTeaserTitle(self):
        return self.data.teasertitle

    def getTeaserDesc(self):
        return self.data.teaserdesc

    @property
    @memoize
    def internal_obj(self):
        state = getMultiAdapter((self.context, self.request),
                              name="plone_portal_state")
        portal = state.portal()
        object_path = self.data.internal_target

        if isinstance(object_path, unicode):
            object_path = object_path.encode('utf8')

        if object_path is None or len(object_path) == 0:
            return None
        #XXX: we have to cut off the /
        if object_path[0] == '/':
            object_path = object_path[1:]
        return portal.restrictedTraverse(object_path, default=None)

    @property
    @memoize
    def image_tag(self):
        if self.data.image:
            state = getMultiAdapter((self.context, self.request),
                                  name="plone_portal_state")
            portal = state.portal()
            assignment_url = \
                    portal.unrestrictedTraverse(
                self.data.assignment_context_path).absolute_url()
            return "<img src='%s/%s/@@image' alt=''/>" % \
                   (assignment_url,
                    self.data.__name__
                    )
        return ''


class AddForm(form.AddForm):
    fields = field.Fields(ITeaserPortlet)

    label = _(u"Add Teaser Portlet")
    description = _(u"Shows the given infos on the front-page.")

    def __init__(self, context, request):
        super(AddForm, self).__init__(context, request)
        self._finishedAdd = None
        self.status = None

    def updateWidgets(self):
        self.fields['teaserdesc'].widgetFactory[INPUT_MODE] = WysiwygFieldWidget
        self.fields['internal_target'].widgetFactory = ContentTreeFieldWidget

        super(AddForm, self).updateWidgets()

    def nextURL(self):
        editview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(editview))
        url = str(getMultiAdapter((context, self.request),
                                  name=u"absolute_url"))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"),
                             name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(nextURL)
        return ''

    def add(self, obj):
        ob = self.context.add(obj)
        self._finishedAdd = True
        return ob

    def create(self, data):

        portal_path_l = len(
            self.context.portal_url.getPortalObject().getPhysicalPath())
        assignment_context_path = '/'.join(
            self.context.__parent__.getPhysicalPath()[portal_path_l:])

        return Assignment(
            assignment_context_path=assignment_context_path, **data)


class EditForm(form.EditForm):
    form_fields = field.Fields(ITeaserPortlet)

    label = _(u"Edit Teaser Portlet")
    description = _(u"Shows the given infos on the front-page.")

    def updateWidgets(self):
        self.fields['teaserdesc'].widgetFactory[INPUT_MODE] = WysiwygFieldWidget
        self.fields['internal_target'].widgetFactory = ContentTreeFieldWidget
        super(EditForm, self).updateWidgets()
