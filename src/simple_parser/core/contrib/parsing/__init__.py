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
    """
    :param html: html string
    :param url: url string. This param is required if it's nessesary to get
     absolute urls
    :param using: parser_type (use keys from PARSER_MAPPING).
    :return: parser object by using param or using DEFAULT_PARSER from settings
     or DefaultParser
    """
    using = using or getattr(settings, 'DEFAULT_PARSER', 'default')
    parser = PARSER_MAPPING.get(using)
    if not parser:
        raise ImproperlyConfigured('Указан несуществующий парсер')
    return parser(html, url)
