from ftw.upgrade import UpgradeStep


class UnhideLogoViewlet(UpgradeStep):
    """Unhide logo viewlet.
    """

    def __call__(self):
        self.install_upgrade_profile()
