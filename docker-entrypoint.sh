#!/bin/sh

flask db upgrade

if test "$FLASK_ENV" = "development"; then
  gunicorn --reload -c dev.config.py app:app
else
  gunicorn -c config.py app:app
fi