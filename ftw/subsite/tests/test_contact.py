from ftw.builder import Builder
from ftw.builder import create
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from ftw.testing import IS_PLONE_5
from unittest import TestCase
import email
import transaction


class TestContactFrom(TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):

        self.portal = self.layer['portal']
        self.subsite = create(Builder('subsite')
                              .titled(u'S\xfcbsite')
                              .having(from_email=u'blubber@blubb.ch',
                                      from_name=u'Subsite'))

    @browsing
    def test_contact_everything_ok(self, browser):
        browser.login().visit(self.subsite, view='contact-info')
        browser.fill({'form.widgets.sender': u'hans peter',
                      'form.widgets.email': u'test@test.com',
                      'form.widgets.subject': u'Testsubject',
                      'form.widgets.message': u'Lorem ipsum dolor sit amet'}
                     ).submit()

        mh = self.portal.MailHost
        self.assertEqual(len(mh.messages), 1)

        msg = email.message_from_string(mh.messages[0])
        self.assertEqual(msg.get('From'), 'Subsite <blubber@blubb.ch>')
        self.assertEqual(msg.get('reply-to'), u'hans peter <test@test.com>')
        sub = msg.get('Subject')
        self.assertEqual(sub.encode('utf8'), '=?utf-8?q?Testsubject?=')
        self.assertEqual(
            ('hans peter (test@test.com) sends you a message from your site '
             'S=C3=BCbsite (http://nohost/plone/subsite):'
             'Lorem ipsum dolor sit amet'),
            msg.get_payload().replace('=\n', '').replace('\n', ''))

    @browsing
    def test_contact_cancel(self, browser):
        browser.login().visit(self.subsite, view='contact-info')
        browser.find_button_by_label('Cancel').click()
        self.assertEqual(browser.url, self.subsite.absolute_url())

    @browsing
    def test_contact_portal(self, browser):
        self.portal.setTitle('Test\xc3\xbc')
        self.portal.manage_changeProperties(
            email_from_address='site@nohost.com')
        self.portal.manage_changeProperties(email_from_name='Ploneroot')
        transaction.commit()

        browser.login().visit(self.portal, view='@@contact-info')

        browser.fill({'form.widgets.sender': u'hans peter',
                      'form.widgets.email': u'test@test.com',
                      'form.widgets.subject': u'Testsubject',
                      'form.widgets.message': u'Lorem ipsum dolor sit amet'}
                     ).submit()

        mh = self.portal.MailHost
        self.assertEqual(len(mh.messages), 1)

        msg = email.message_from_string(mh.messages[0])
        if IS_PLONE_5:
            self.assertEqual(msg.get('From'), '<site@nohost.com>')
        else:
            self.assertEqual(msg.get('From'), 'Ploneroot <site@nohost.com>')

        self.assertEqual(msg.get('reply-to'), u'hans peter <test@test.com>')

        sub = msg.get('Subject')
        self.assertEqual(sub.encode('utf8'), '=?utf-8?q?Testsubject?=')
        self.assertEqual(
            ('hans peter (test@test.com) sends you a message from your site '
             'Test=C3=BC (http://nohost/plone):'
             'Lorem ipsum dolor sit amet'),
            msg.get_payload().replace('=\n', '').replace('\n', ''))

    @browsing
    def test_contact_invalid_email(self, browser):
        browser.login().visit(self.subsite, view='contact-info')
        browser.fill({'form.widgets.sender': u'hans peter',
                      'form.widgets.email': u'test@test',
                      'form.widgets.subject': u'Testsubject',
                      'form.widgets.message': u'Lorem ipsum dolor sit amet'}
                     ).submit()
        self.assertIn(
            '<div class="error">Your E-mail address is not valid.</div>',
            browser.contents)
