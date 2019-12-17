from ftw.upgrade import UpgradeStep


class UpdateBundleRegistration(UpgradeStep):
    """Update bundle registration.
    """

    def __call__(self):
        self.install_upgrade_profile()
