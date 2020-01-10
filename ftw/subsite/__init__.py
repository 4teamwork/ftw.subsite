from Products.Archetypes import atapi
from Products.CMFCore import utils as cutils
from Products.CMFPlone.utils import getFSVersionTuple
from ftw.subsite import config
from zope.i18nmessageid import MessageFactory


IS_PLONE_5 = getFSVersionTuple() > (5, )

_ = MessageFactory('ftw.subsite')


def initialize(context):
    """Initializer called when used as a Zope 2 product.

    This is referenced from configure.zcml. Regstrations as a "Zope 2 product"
    is necessary for GenericSetup profiles to work, for example.

    Here, we call the Archetypes machinery to register our content types
    with Zope and the CMF.
    """

    content_types, constructors, _ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        cutils.ContentInit('%s: %s' % (config.PROJECTNAME, atype.portal_type),
                          content_types=(atype,),
                          permission=config.ADD_PERMISSIONS[atype.portal_type],
                          extra_constructors=(constructor,),
                          ).initialize(context)
