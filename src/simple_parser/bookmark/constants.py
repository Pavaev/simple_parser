from enumfields import Enum


class EmbeddedMetadataTypes(Enum):
    DEFAULT = 'default'
    OPENGRAPH = 'opengraph'
    JSON_LD = 'json-ld'
    SCHEMA_ORG = 'schema.org'

    class Labels:
        DEFAULT = 'Стандартный (метатеги)'
        OPENGRAPH = 'Open Graph'
        JSON_LD = 'JSON-LD'
        SCHEMA_ORG = 'Schema.org'
