from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2
from zope.configuration import xmlconfig


class FtwSubsiteIntegrationLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ftw.subsite
        xmlconfig.file('configure.zcml', ftw.subsite,
                       context=configurationContext)

        xmlconfig.file('overrides.zcml', ftw.subsite,
                       context=configurationContext)

        import plone.app.portlets
        xmlconfig.file('configure.zcml', plone.app.portlets,
                       context=configurationContext)

        # installProduct() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2 products,
        # using <five:registerPackage /> in ZCML.
        z2.installProduct(app, 'plone.app.portlets')
        z2.installProduct(app, 'ftw.subsite')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'ftw.subsite:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


FTW_SUBSITE_FIXTURE = FtwSubsiteIntegrationLayer()
FTW_SUBSITE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_SUBSITE_FIXTURE,), name="FtwSubsite:Integration")
FTW_SUBSITE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FTW_SUBSITE_FIXTURE,), name="FtwSubsite:Functional")
