from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .parser import (DefaultParser, JSONLDParser, OpenGraphParser,
                     SchemaOrgParser)

PARSER_MAPPING = {
    'default': DefaultParser,
    'opengraph': OpenGraphParser,
    'json-ld': JSONLDParser,
    'schema.org': SchemaOrgParser,
}


def get_parser(html, url=None, using=None):
    using = using or getattr(settings, 'DEFAULT_PARSER', 'default')
    parser = PARSER_MAPPING.get(using)
    if not parser:
        raise ImproperlyConfigured('Указан несуществующий парсер')
    return parser(html, url)
