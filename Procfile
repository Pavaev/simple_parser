web: cd src && gunicorn simple_parser.wsgi:application --log-file -
worker: cd src && celery worker --app=simple_parser.celery:app -E -l info
