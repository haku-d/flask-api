# flask-api

## Good resource to quicky and easily build back-end api for any front-end application

## Technology stack

-   Docker
-   MariaDB
-   Flask (SQLAlchemy, Migration)
-   Gunicorn

## Build docker image

1. Modify `build.sh` by updating gitlab container package registry info
2. Run command `./build.sh X.X.X` with `X.X.X` is your specific version of new image

## Install and run locally

1. `python -m venv venv`
2. `source venv/bin/active` <~ for macos only
3. `./start.sh`
