#!/usr/bin/env bash
# exit on error
set -o errexit

# Ensure Python 3.13 is used
export PYTHON_VERSION=3.13.4

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
