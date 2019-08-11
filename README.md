My test task for job interview

This is a simple parser for html embedded metadata for title, description and favicon.
There is a four types of parsers: OpenGraph, JSON-LD, Schema.org and default(using <meta> tags).
You can select type of a parser by DEFAULT_PARSER environment variable.

Allowed values for DEFAULT_PARSER:
- opengraph
- json-ld
- schema.org
- default

Installation:
- pip install -r requirements.txt
- create .env file in src/
- create local_settings.py in src/simple_parser/settings/
- run python src/manage.py migrate

default settings file is production.py.
set DJANGO_SETTINGS_MODULE=simple_parser.settings.local_settings
(or development) if you want to use another settings 
