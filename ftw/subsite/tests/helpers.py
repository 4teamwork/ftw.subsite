from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
import transaction


def introduce_language_subsites(*subsites):
    intids = getUtility(IIntIds)

    for subsite in subsites:
        ids = [intids.getId(obj) for obj in subsites]
        ids.remove(intids.getId(subsite))
        subsite.language_references = [RelationValue(id_) for id_ in ids]

        transaction.commit()
