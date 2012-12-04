import unittest2 as unittest
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.testing.z2 import Browser
from plone.app.testing import login, TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD, setRoles, logout
import transaction
from StringIO import StringIO

class TestSubsite(unittest.TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        file_ = open("../../ftw/subsite/tests/blue.png")
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Reviewer', 'Contributor'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory(
            'Subsite', 'mysubsite', title="Peter", logo=file_.read(), subsite_languages=['de', 'en'])
        subsite = self.portal['mysubsite']
        subsite.invokeFactory(
            'Document', 'mypage', title="MyPage")
        logout()
        transaction.commit()

    def tearDown(self):
        login(self.portal, TEST_USER_NAME)
        self.portal.manage_delObjects(['mysubsite'])
        transaction.commit()

    def test_add_subsite(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        self.browser.open(self.portal.absolute_url() + '/folder_factories')
        button = self.browser.getControl(name="url")
        button.value = [button.options[-1]]
        self.browser.getControl(name="form.button.Add").click()
        file_ = open("../../ftw/subsite/tests/blue.png")
        file_field = self.browser.getControl(name="logo_file")
        file_field.add_file(StringIO(file_.read()), 'image/png', 'blue.png')
        self.browser.getControl(name="title").value = "Testsubsite"
        self.browser.getControl(name="form.button.save").click()
        self.assertEqual(self.browser.url, 'http://nohost/plone/testsubsite/')

    def test_logo_viewlet(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        self.browser.open(self.portal.absolute_url() + '/mysubsite')
        self.assertTrue(
            'http://nohost/plone/mysubsite/@@images' in self.browser.contents)
        self.assertTrue('alt="Peter"' in self.browser.contents)
        self.browser.open(self.portal.absolute_url())
        self.assertTrue("http://nohost/plone/logo.png" in self.browser.contents)

    def test_portlets(self):
        self.browser.open(self.portal.absolute_url() + '/mysubsite')
        self.assertTrue('edit Portlets' not in self.browser.contents)
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        self.browser.open('http://nohost/plone/mysubsite/@@manage-subsiteview')

        self.assertTrue('dashboard-portlets1' in self.browser.contents)
        self.assertTrue('dashboard-portlets2' in self.browser.contents)
        self.assertTrue('dashboard-portlets3' in self.browser.contents)
        self.assertTrue('dashboard-portlets4' in self.browser.contents)
        self.assertTrue('dashboard-portlets5' in self.browser.contents)
        self.assertTrue('dashboard-portlets6' in self.browser.contents)

    def test_teaser(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        self.browser.open('http://nohost/plone/mysubsite/++contextportlets++ftw.subsite.front2/+/ftw.subsite.teaserportlet')
        self.browser.getControl(name="form.buttons.add").click()
        self.assertEqual(self.browser.url, 'http://nohost/plone/mysubsite/++contextportlets++ftw.subsite.front2/+/ftw.subsite.teaserportlet')

        self.browser.getControl(name="form.buttons.cancel_add").click()
        self.assertEqual(self.browser.url, 'http://nohost/plone/mysubsite')
        self.browser.open('http://nohost/plone/mysubsite/++contextportlets++ftw.subsite.front2/+/ftw.subsite.teaserportlet')
        self.browser.getControl(name="form.widgets.teasertitle").value = u"hans"
        self.browser.getControl(name="form.widgets.teaserdesc").value = u"bla bla bla mr. Freeman"
        self.browser.getControl(name="form.widgets.internal_target.widgets.query").value = u"my"
        self.browser.getControl(name="form.widgets.internal_target.buttons.search").click()
        self.browser.getControl("MyPage").selected = True

        file_ = open("../../ftw/subsite/tests/blue.png")
        file_field = self.browser.getControl(name="form.widgets.image")
        file_field.add_file(StringIO(file_.read()), 'image/png', 'blue.png')
        self.browser.getControl(name="form.buttons.add").click()

        self.assertEqual(self.browser.url, "http://nohost/plone/mysubsite")
        self.assertTrue('http://nohost/plone/mysubsite/++contextportlets++ftw.subsite.front2/hans/@@image' in self.browser.contents)
        self.assertTrue('teaser_portlet' in self.browser.contents)
        self.assertTrue('bla bla bla mr. Freeman' in self.browser.contents)

        self.browser.open('http://nohost/plone/mysubsite/++contextportlets++ftw.subsite.front2/hans/edit')
        self.browser.getControl(name="form.buttons.apply").click()
        self.assertIn('Data successfully updated.', self.browser.contents)

        self.browser.open('http://nohost/plone/mysubsite/++contextportlets++ftw.subsite.front2/hans/@@image')
        self.assertIn(('content-type', 'image/png'), self.browser.mech_browser.response()._headers.items())

    def test_languageswitcher(self):
        login(self.portal, TEST_USER_NAME)
        file_ = open("../../ftw/subsite/tests/blue.png")
        self.portal.invokeFactory(
            'Subsite', 'en', title="English", logo=file_.read(), subsite_languages=['de', 'en'])
        transaction.commit()

        self.browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        self.browser.open(self.portal.absolute_url() + '/mysubsite')
        self.browser.getLink('English').click()
        self.assertEqual(self.browser.url, 'http://nohost/plone/en')
        self.browser.open(self.portal.absolute_url() + '/mysubsite')
        self.browser.getLink('German').click()
        self.assertEqual(self.browser.url, self.portal.absolute_url() + '/mysubsite')
        self.browser.open(self.portal.absolute_url() + '/mysubsite/switchLanguage?set_language=')
        self.assertEqual(self.browser.url, self.portal.absolute_url() + '/en')
        self.browser.open(self.portal.absolute_url() + '/mysubsite/switchLanguage?blubb=hahaha')
        self.assertEqual(self.browser.url, self.portal.absolute_url() + '/mysubsite')
