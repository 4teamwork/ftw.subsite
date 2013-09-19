from ftw.builder.archetypes import ArchetypesBuilder
from ftw.builder import builder_registry


class SubsiteBuilder(ArchetypesBuilder):

    portal_type = 'Subsite'

    def with_language(self, language_code):
        if 'title' not in self.arguments:
            return self.having(forcelanguage=language_code,
                               title=language_code)
        else:
            return self.having(forcelanguage=language_code)


builder_registry.register('subsite', SubsiteBuilder)
