from ftw.subsite.testing import FTW_SUBSITE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
import unittest2 as unittest
import transaction
from zope.component import getUtility, getMultiAdapter
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from ftw.subsite.portlets import teaserportlet

class TestSubsite(unittest.TestCase):

    layer = FTW_SUBSITE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

        self.subsite = self._create_subsite()

        transaction.commit()

    def _create_subsite(self):
        subsite = self.portal.get(self.portal.invokeFactory(
            'Subsite',
            'mysubsite',
            title="Peter"))
        transaction.commit()

        return subsite

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

    def tearDown(self):
        self.portal.manage_delObjects(['mysubsite'])
        transaction.commit()

    def test_view_render(self):
        self.browser.open(self.subsite.absolute_url())
        for item in range(1, 6):
            self.assertIn('<div id="subsite-column-%s" class="column">' % str(item), self.browser.contents)


    def test_manageview_render(self):
        self._auth()
        self.browser.open(self.subsite.absolute_url() + '/manage-subsiteview')
        for item in range(1, 6):
            self.assertIn('<div id="subsite-column-%s" class="column">' % str(item), self.browser.contents)

    def test_view_authorized(self):
        self._auth()
        self.browser.open(self.subsite.absolute_url())
        self.assertIn(' <h1 id="parent-fieldname-title" class="documentFirstHeading', self.browser.contents)
        self.assertIn('<div class="contentActions">', self.browser.contents)

    def test_view_anonymous(self):
        self.browser.open(self.subsite.absolute_url())
        self.assertNotIn(' <h1 id="parent-fieldname-title" class="documentFirstHeading', self.browser.contents)

    def test_drop_parent_portlets(self):
        manager = getUtility(IPortletManager, name='ftw.subsite.front1')
        mapping = getMultiAdapter((self.subsite, manager),
                                  IPortletAssignmentMapping).__of__(self.subsite)

        mapping['myportlet'] = teaserportlet.Assignment(teasertitle='MyPortlet',
                 teaserdesc='Lorem Ipsum')

        housi = self.subsite.get(self.subsite.invokeFactory('Subsite', 'hans', title="Housi"))
        housi.processForm()
        transaction.commit()
        self.browser.open(housi.absolute_url())
        self.assertNotIn('MyProtlet', self.browser.contents)
