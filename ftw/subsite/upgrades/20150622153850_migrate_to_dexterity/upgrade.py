from ftw.subsite.migration.migration import SubsiteMigration
from ftw.upgrade import UpgradeStep


class MigrateToDexterity(UpgradeStep):
    """Migrate to dexterity.
    """

    def __call__(self):
        self.install_upgrade_profile()
        self.setup_install_profile('profile-ftw.simplelayout:default')
        SubsiteMigration(self.portal)()
