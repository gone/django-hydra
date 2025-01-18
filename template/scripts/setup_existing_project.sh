#!/bin/bash
echo "Setting up a previously created project"

## Set mydir to the directory containing the script
## The ${var%pattern} format will remove the shortest match of
## pattern from the end of the string. Here, it will remove the
## script's name,. leaving only the directory.
thisdir="${0%/*}"


cp $thisdir/../.env.example $thisdir/../.env;
$thisdir/setup_python.sh
# allow python to setup the venv before switching into it
direnv allow . && eval "$(direnv export bash)"
$thisdir/setup_js.sh
$thisdir/setup_database.sh

echo "omae wa mou shindeiru"

$thisdir/setup_github.sh

chmod +x manage.py
poetry run pre-commit install

unset DJANGO_SECRET_KEY

#todo - git flow init
echo "-------------------------------------------------------------"
echo "Maybe The Real setup_existing_project.sh Was the Friends We Made Along the Way"
echo "-------------------------------------------------------------"
