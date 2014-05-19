from StringIO import StringIO
from ftw.subsite.portlets import teaserportlet
from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.namedfile.file import NamedImage
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from plone.testing.z2 import Browser
from plone.uuid.interfaces import IUUID
from pyquery import PyQuery as pq
from zope.component import getMultiAdapter
from zope.component import getUtility
import transaction
import unittest2 as unittest
import zope.event
import zope.lifecycleevent

class TestSubsite(unittest.TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

        self.subsite = self._create_subsite()
        self.page = self.subsite.get(
            self.subsite.invokeFactory('Document',
                                   'mypage',
                                   title="MyPage"
                                   ))
        transaction.commit()

    def tearDown(self):
        self.portal.manage_delObjects(['mysubsite'])
        transaction.commit()

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

    def _create_subsite(self):
        subsite = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'mysubsite',
            title="MySubsite"))

        transaction.commit()
        return subsite

    def _create_portlet(self):
        image1 = NamedImage(open("../../ftw/subsite/tests/blue.png"), contentType='image/png',
                        filename=u'blue.png')

        assignment = teaserportlet.Assignment(
            assignment_context_path='++contextportlets++ftw.subsite.front1',
            teasertitle=u'hans',
            teaserdesc=u'peter',
            internal_target=IUUID(self.page),
            image=image1
            )
        zope.event.notify(zope.lifecycleevent.ObjectCreatedEvent(assignment))
        return assignment

    def _get_renderer(self):
        context = self.subsite
        request = self.layer['request']
        view = context.restrictedTraverse('@@plone')
        assignment = self._create_portlet()
        manager = getUtility(
            IPortletManager, name='plone.rightcolumn', context=context)
        mapping = getMultiAdapter((context, manager),
                                  IPortletAssignmentMapping, context=self.subsite)
        mapping['hans'] = assignment
        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        return renderer

    def test_portlet_type_registered(self):
        portlet = getUtility(
            IPortletType, name='ftw.subsite.teaserportlet')
        self.assertEquals(
            portlet.addview, 'ftw.subsite.teaserportlet')

    def test_interfaces(self):
        portlet = teaserportlet.Assignment()
        self.failUnless(
            teaserportlet.ITeaserPortlet.providedBy(portlet))

    def test_add_form_send_empty(self):
        self._auth()
        self.browser.open(self.subsite.absolute_url() + '/++contextportlets++ftw.subsite.front2/+/ftw.subsite.teaserportlet')
        self.browser.getControl(name="form.buttons.add").click()
        self.assertEqual(self.browser.url, self.subsite.absolute_url() + '/++contextportlets++ftw.subsite.front2/+/ftw.subsite.teaserportlet')

    def test_add_form_send_cancel(self):
        self._auth()
        self.browser.open(self.subsite.absolute_url() + '/++contextportlets++ftw.subsite.front2/+/ftw.subsite.teaserportlet')
        self.browser.getControl(name="form.buttons.cancel_add").click()
        self.assertEqual(self.browser.url, self.subsite.absolute_url())

    def test_add_form_send_without_interaltarget(self):
        self._auth()
        self.browser.open(self.subsite.absolute_url() + '/++contextportlets++ftw.subsite.front2/+/ftw.subsite.teaserportlet')
        self.browser.getControl(name="form.widgets.teasertitle").value = u"hans"
        self.browser.getControl(name="form.widgets.teaserdesc").value = u"bla bla bla mr. Freeman"
        file_ = open("../../ftw/subsite/tests/blue.png")
        file_field = self.browser.getControl(name="form.widgets.image")
        file_field.add_file(StringIO(file_.read()), 'image/png', 'blue.png')
        self.browser.getControl(name="form.buttons.add").click()
        self.assertEqual(self.browser.url, "http://nohost/plone/mysubsite")
        self.assertFalse('<a href="http://nohost/plone/mysubsite/mypage">' in self.browser.contents)

    def test_add_form_send_with_interaltarget(self):
        self._auth()
        self.browser.open(self.subsite.absolute_url() + '/++contextportlets++ftw.subsite.front2/+/ftw.subsite.teaserportlet')
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

        doc = pq(self.browser.contents)
        link = doc('a[href="http://nohost/plone/mysubsite/mypage"]')
        self.assertTrue(link, 'Teaser portlet Link "MyPage" missing.')

    def test_edit_form(self):
        self._auth()
        self.browser.open(self.subsite.absolute_url() + '/++contextportlets++ftw.subsite.front2/+/ftw.subsite.teaserportlet')
        self.browser.getControl(name="form.widgets.teasertitle").value = u"hans"
        self.browser.getControl(name="form.widgets.teaserdesc").value = u"bla bla bla mr. Freeman"
        self.browser.getControl(name="form.widgets.internal_target.widgets.query").value = u"my"
        self.browser.getControl(name="form.widgets.internal_target.buttons.search").click()
        self.browser.getControl("MyPage").selected = True
        file_ = open("../../ftw/subsite/tests/blue.png")
        file_field = self.browser.getControl(name="form.widgets.image")
        file_field.add_file(StringIO(file_.read()), 'image/png', 'blue.png')
        self.browser.getControl(name="form.buttons.add").click()
        self.browser.open(self.subsite.absolute_url()+'/++contextportlets++ftw.subsite.front2/hans/edit')
        self.browser.getControl(name="form.buttons.apply").click()
        self.assertIn('Data successfully updated.', self.browser.contents)

    def test_assignment_portlettitle(self):
        portlet = self._create_portlet()
        self.assertEqual('hans', portlet.title)

    def test_renderer_image_tag(self):
        renderer = self._get_renderer()
        markup = renderer.image_tag
        self.assertIn(
            'http://nohost/plone/++contextportlets++ftw.subsite.front1/hans/@@image',
            markup)

    def test_renderer_internal_url(self):
        renderer = self._get_renderer()
        self.assertEqual(self.page.absolute_url(), renderer.internal_url)

    def test_image_view(self):
        self._auth()
        self.browser.open(self.subsite.absolute_url() + '/++contextportlets++ftw.subsite.front2/+/ftw.subsite.teaserportlet')
        self.browser.getControl(name="form.widgets.teasertitle").value = u"hans"
        self.browser.getControl(name="form.widgets.teaserdesc").value = u"bla bla bla mr. Freeman"
        self.browser.getControl(name="form.widgets.internal_target.widgets.query").value = u"my"
        self.browser.getControl(name="form.widgets.internal_target.buttons.search").click()
        self.browser.getControl("MyPage").selected = True
        file_ = open("../../ftw/subsite/tests/blue.png")
        file_field = self.browser.getControl(name="form.widgets.image")
        file_field.add_file(StringIO(file_.read()), 'image/png', 'blue.png')
        self.browser.getControl(name="form.buttons.add").click()
        self.browser.open('http://nohost/plone/mysubsite/++contextportlets++ftw.subsite.front2/hans/@@image')
        self.assertEqual([
            ('status', '200 Ok'), ('content-length', '0'),
            ('content-type', 'image/png'),
            ('cache-control', 'max-age=86400')],
            self.browser.mech_browser.response()._headers.items())
