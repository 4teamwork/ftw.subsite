from ftw.subsite.migration.migration import SubsiteMigration
from ftw.upgrade import UpgradeStep


class MigrateToDexterity(UpgradeStep):
    """Migrate to dexterity.
    """

    def __call__(self):
        self.setup_install_profile('profile-ftw.simplelayout:default')
        self.setup_install_profile('profile-collective.z3cform.widgets:default')
        self.install_upgrade_profile()
        SubsiteMigration(self.portal)()
