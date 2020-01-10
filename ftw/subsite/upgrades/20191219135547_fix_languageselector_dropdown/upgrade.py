from ftw.subsite import IS_PLONE_5
from ftw.upgrade import UpgradeStep


class FixLanguageselectorDropdown(UpgradeStep):
    """Fix languageselector dropdown.
    """

    def __call__(self):
        if IS_PLONE_5:
            self.install_upgrade_profile(['plone.app.registry'])
        else:
            self.install_upgrade_profile(['jsregistry'])
