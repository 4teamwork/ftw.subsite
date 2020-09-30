from ftw.upgrade import UpgradeStep
from Products.CMFPlone.utils import getFSVersionTuple

PLONE5 = getFSVersionTuple() >= (5, 0)


class RemoveObsoleteBehaviours(UpgradeStep):
    """Remove obsolete behaviours.
    """

    def __call__(self):
        if PLONE5:
            self.install_upgrade_profile()
