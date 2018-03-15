#!/bin/bash -xe

flake8 bedrock lib tests
python manage.py version
python manage.py migrate --noinput --database bedrock
py.test lib bedrock
py.test -r a -m smoke tests/redirects
