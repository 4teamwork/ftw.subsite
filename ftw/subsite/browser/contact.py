from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from email.header import Header
from email.mime.text import MIMEText
from ftw.subsite import _
from ftw.subsite import IS_PLONE_5
from plone.app.layout.navigation.root import getNavigationRoot
from plone.dexterity.utils import safe_utf8
from z3c.form import form, field, button
from z3c.form.validator import SimpleFieldValidator
from z3c.form.validator import WidgetValidatorDiscriminators
from zope import schema
from zope.component import provideAdapter
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import Invalid
import re


class IContactForm(Interface):
    """Interface for z3c.form"""
    sender = schema.TextLine(title=_(u"Sender_Name", default=u"Name"),
                             required=True,
                             description=_(u"help_Sender", default="Please enter your Name"))
    email = schema.TextLine(title=_(u"mail_address", default="E-Mail"),
                            required=True,
                            description=_(u"help_mail_address", default="Please enter your e-mail"))
    subject = schema.TextLine(title=_(u"label_subject", default="Subject"),
                              required=True,
                              description=_(u"help_subject", default="Please enter a Subject"))
    message = schema.Text(title=_(u"label_message", default="Message"),
                          required=True,
                          description=_(u"help_message", default="Please enter a Message"))


class ContactForm(form.Form):
    label = _(u"label_send_feedback", default=u"Send Feedback")
    fields = field.Fields(IContactForm)
    # don't use context to get widget data
    ignoreContext = True

    @button.buttonAndHandler(_(u'Send Mail'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            return

        message = data.get('message')
        email = data.get('email')
        subject = data.get('subject')
        sender = data.get('sender')
        self.send_feedback(email, subject, message, sender)
        msg = _(u'info_email_sent', default=u'The email was sent.')
        IStatusMessage(self.request).addStatusMessage(msg, type='info')
        return self.redirect()

    @button.buttonAndHandler(_(u'button_cancel', default=u'Cancel'))
    def handle_cancel(self, action):
        return self.redirect()

    def redirect(self):
        """Redirect back
        """
        url = self.context.absolute_url()
        return self.request.RESPONSE.redirect(url)

    def send_feedback(self, recipient, subject, message, sender):
        """Send a feedback email to the email address defined in subsite.
        """
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        nav_root = None
        if not '/'.join(portal.getPhysicalPath()) == getNavigationRoot(self.context):
            nav_root = self.context.restrictedTraverse(
                getNavigationRoot(self.context))
        if nav_root:
            site_title = nav_root.Title().decode('utf-8')
            site_url = nav_root.absolute_url()
        else:
            site_title = portal.Title().decode('utf-8')
            site_url = portal.absolute_url()

        message = translate(
            u'feedback_mail_text',
            domain='ftw.subsite',
            default=u'${sender} sends you a message from your site ${site_title} (${site_url}):\n${msg}',
            context=self.request,
            mapping={'sender': u"%s (%s)" % (sender, recipient),
                     'msg': message,
                     'site_title': site_title,
                     'site_url': site_url})

        default_from_name = portal.getProperty('email_from_name', '')
        default_from_email = portal.getProperty('email_from_address', '')

        if nav_root:
            email_from_name = getattr(nav_root, 'from_name', default_from_name)
            email_from_email = getattr(nav_root, 'from_email', default_from_email)
        else:
            email_from_name = default_from_name
            email_from_email = default_from_email

        if IS_PLONE_5:
            from plone import api
            reg = api.portal.get_tool('portal_registry')
            from_email_field = reg._records.get('plone.email_from_address')
            if not email_from_email and not from_email_field.value:
                # especially for testing reasons we need to set a value here
                # if none is registered on the page in plone5
                from_email_field._set_value('site@nohost.com')
                email_from_email = from_email_field.value

            email_from_email = (email_from_email or
                                reg._records.get('plone.email_from_address').value)
            email_from_name = (email_from_name or
                               reg._records.get('plone.email_from_name').value)

        # send the message
        self.send_mail(email_from_name, email_from_email, email_from_email,
                       subject, message, recipient, sender)

    def send_mail(self, name_from, mail_from, mail_to, mail_subject,
                  message_text, reply_mail, reply_name):
        """Send mail using plone mailhost (all input strings need to be utf-8).
        """
        if not name_from:
            name_from = ''
        # Put together the mail parts
        msg = MIMEText(safe_utf8(message_text), 'plain', 'utf-8')
        msg['From'] = '{} <{}>'.format(safe_utf8(name_from),
                                       safe_utf8(mail_from))
        msg['To'] = safe_utf8(mail_to)
        msg['Subject'] = Header(safe_utf8(mail_subject), 'utf-8')
        msg['reply-to'] = '{} <{}>'.format(safe_utf8(reply_name),
                                           safe_utf8(reply_mail))

        # Get mailhost and send to mail_to
        mailhost = getToolByName(self.context, 'MailHost')
        mailhost.send(msg)


class AddressesValidator(SimpleFieldValidator):
    """Validator for validating the e-mail addresses field
    """

    MAIL_EXPRESSION = r"^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=" +\
        "?^_`{}|~]+@(([0-9a-z]([0-9a-z-]*[0-9a-z])?" +\
        "\.)+[a-z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$"

    def __init__(self, *args, **kwargs):
        super(AddressesValidator, self).__init__(*args, **kwargs)
        self.email_expression = re.compile(AddressesValidator.MAIL_EXPRESSION,
                                           re.IGNORECASE)

    def validate(self, value):
        """Validates the `value`, expects a list of carriage-return-separated
        email addresses.
        """
        super(AddressesValidator, self).validate(value)
        if value:
            address = value.strip()
            self._validate_addresses(address)

    def _validate_addresses(self, address):
        """E-Mail address validation
        """
        address = address.strip()
        if not self.email_expression.match(address):
            msg = _(u'error_invalid_addresses',
                    default=u'Your E-mail address is not valid.')
            raise Invalid(msg)


WidgetValidatorDiscriminators(AddressesValidator,
                              field=IContactForm['email'])
provideAdapter(AddressesValidator)
