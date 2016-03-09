from ftw.builder.archetypes import ArchetypesBuilder
from ftw.builder import builder_registry
from ftw.builder.dexterity import DexterityBuilder
import os


class SubsiteBuilder(ArchetypesBuilder):

    portal_type = 'Subsite'

    def with_language(self, language_code):
        if 'title' not in self.arguments:
            return self.having(forcelanguage=language_code,
                               title=language_code)
        else:
            return self.having(forcelanguage=language_code)

    def with_dummy_logo(self):
        png_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'blue.png',
        )
        logo = open(png_file, 'r')
        self.arguments['logo'] = logo
        return self

builder_registry.register('subsite', SubsiteBuilder)


class ExampleDxTypeBuilder(DexterityBuilder):
    portal_type = 'ExampleDxType'

builder_registry.register('example dx type', ExampleDxTypeBuilder)
