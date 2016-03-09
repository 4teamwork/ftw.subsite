from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing import FunctionalSplinterTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.testing import z2
from zope.configuration import xmlconfig
import ftw.subsite.tests.builders


class FtwSubsiteIntegrationLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '  <include package="ftw.subsite.tests" />'
            '  <include package="collective.MockMailHost" />'
            '</configure>',
            context=configurationContext)

        # installProduct() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2 products,
        # using <five:registerPackage /> in ZCML.
        z2.installProduct(app, 'plone.app.portlets')
        z2.installProduct(app, 'ftw.subsite')
        z2.installProduct(app, 'collective.MockMailHost')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'ftw.subsite:default')
        applyProfile(portal, 'collective.MockMailHost:default')
        applyProfile(portal, 'plone.app.dexterity:default')
        applyProfile(portal, 'ftw.subsite.tests:dx_creation')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


class FtwSubsiteWithoutApplyProfileLayer(FtwSubsiteIntegrationLayer):
    """Special layer, which does not install the ftw.subsite profile.
    This way the ftw.subsite browserlay will net be installed
    """

    def setUpPloneSite(self, portal):

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


FTW_SUBSITE_FIXTURE = FtwSubsiteIntegrationLayer()
FTW_SUBSITE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_SUBSITE_FIXTURE,), name="FtwSubsite:Integration")
FTW_SUBSITE_FUNCTIONAL_TESTING = FunctionalSplinterTesting(
    bases=(FTW_SUBSITE_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="FtwSubsite:Functional")

FTW_SUBSITE_SPECIAL_FIXTURE = FtwSubsiteWithoutApplyProfileLayer()
FTW_SUBSITE_SPECIAL_FUNCTIONAL_TESTING = FunctionalSplinterTesting(
    bases=(FTW_SUBSITE_SPECIAL_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="FtwSubsite:SpecialFunctional")
