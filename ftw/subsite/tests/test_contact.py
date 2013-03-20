import unittest2 as unittest
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.testing.z2 import Browser
import transaction


class TestContactFrom(unittest.TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):

        self.portal = self.layer['portal']
        self.subsite = self._create_subsite()
        transaction.commit()
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def _create_subsite(self):
        subsite = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'mysubsite',
            title="Peter",
            ))
        subsite.setFromEmail("blubber@blubb.ch")
        subsite.setFromName("Subsite")
        return subsite

    def test_contact_everything_ok(self):
        self.browser.open(self.subsite.absolute_url()+'/contact-info')
        self.browser.getControl(name='form.widgets.sender').value = 'hans peter'
        self.browser.getControl(name='form.widgets.email').value = 'test@test.com'
        self.browser.getControl(name='form.widgets.subject').value = 'Testsubject'
        self.browser.getControl(name='form.widgets.message').value = 'Lorem ipsum dolor sit amet'
        self.browser.getControl(name="form.buttons.53656e64204d61696c").click()
        mh = self.portal.MailHost
        self.assertEqual(len(mh.messages), 1)
        msg = mh.messages[0]
        self.assertEqual(msg.get('From'), 'Subsite <blubber@blubb.ch>')
        self.assertEqual(msg.get('reply-to'), u'hans peter <test@test.com>')
        sub = msg.get('Subject')
        self.assertEqual(sub.encode('utf8'), 'Testsubject')
        self.assertEqual(msg.get_payload(), 'hans peter (test@test.com) sends you a message \
from your site Peter(http://=\nnohost/plone/mysubsite):\nLorem ipsum dolor sit amet')

    def test_contact_cancel(self):
        self.browser.open(self.subsite.absolute_url()+'/contact-info')
        self.browser.getControl(name="form.buttons.button_cancel").click()
        self.assertEqual(self.browser.url, self.subsite.absolute_url())

    def test_contact_portal(self):
        self.portal.setTitle('Test')
        self.portal.manage_changeProperties(email_from_address='site@nohost.com')
        self.portal.manage_changeProperties(email_from_name='Ploneroot')
        transaction.commit()

        self.browser.open(self.portal.absolute_url()+'/@@contact-info')
        self.browser.getControl(name='form.widgets.sender').value = 'hans peter'
        self.browser.getControl(name='form.widgets.email').value = 'test@test.com'
        self.browser.getControl(name='form.widgets.subject').value = 'Testsubject'
        self.browser.getControl(name='form.widgets.message').value = 'Lorem ipsum dolor sit amet'
        self.browser.getControl(name="form.buttons.53656e64204d61696c").click()
        mh = self.portal.MailHost
        self.assertEqual(len(mh.messages), 1)
        msg = mh.messages[0]
        self.assertEqual(msg.get('From'), 'Ploneroot <site@nohost.com>')
        self.assertEqual(msg.get('reply-to'), u'hans peter <test@test.com>')
        sub = msg.get('Subject')
        self.assertEqual(sub.encode('utf8'), 'Testsubject')
        self.assertEqual(msg.get_payload(), 'hans peter (test@test.com) sends you a message from your site Test(http://n=\nohost/plone):\nLorem ipsum dolor sit amet')

    def test_contact_invalid_email(self):
        self.browser.open(self.subsite.absolute_url()+'/contact-info')
        self.browser.getControl(name='form.widgets.sender').value = 'hans peter'
        self.browser.getControl(name='form.widgets.email').value = 'test@test'
        self.browser.getControl(name='form.widgets.subject').value = 'Testsubject'
        self.browser.getControl(name='form.widgets.message').value = 'Lorem ipsum dolor sit amet'
        self.browser.getControl(name="form.buttons.53656e64204d61696c").click()
        self.assertIn('<div class="error">Your e-mailaddress is not valid</div>', self.browser.contents)
