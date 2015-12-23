from ftw.upgrade import UpgradeStep


class AddPermissionForCustomAnalyticsSnippet(UpgradeStep):
    """Add permission for custom analytics snippet.
    """

    def __call__(self):
        self.install_upgrade_profile()
