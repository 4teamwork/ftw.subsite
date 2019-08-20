from ftw.upgrade import UpgradeStep
import pkg_resources


IS_PLONE_5 = pkg_resources.get_distribution('Products.CMFPlone').version >= '5'


class RenameRessourcesFolderToResources(UpgradeStep):
    """Rename ressources folder to resources.
    """

    def __call__(self):
        if IS_PLONE_5:
            self.install_upgrade_profile(steps=['plone.app.registry'])
        else:
            self.install_upgrade_profile(steps=['cssregistry'])
