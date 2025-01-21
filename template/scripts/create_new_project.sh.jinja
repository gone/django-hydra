#!/bin/bash
echo "Setting up for a GRRRRREAT DJANGO PROJECT"

## Set mydir to the directory containing the script
## The ${var%pattern} format will remove the shortest match of
## pattern from the end of the string. Here, it will remove the
## script's name,. leaving only the directory.
thisdir="${0%/*}"


echo "Making Virtual Environment for [[project_name]]"
export ENV_NAME="[[project_name]]"

cp $thisdir/../.env.example $thisdir/../.env;
export DJANGO_SETTINGS_MODULE=$ENV_NAME.config.settings.local
export DJANGO_SECRET_KEY="testkey"

$thisdir/setup_python.sh

# Direnv doesn't exist on CI, so install the poetry dependencies manually.
if command -v direnv
then
	# This also sets up the venv.
    direnv allow . && eval "$(direnv export bash)"
fi

$thisdir/setup_js.sh
$thisdir/setup_database.sh
echo "omae wa mou shindeiru"
$thisdir/setup_github.sh

poetry run pre-commit install
chmod +x manage.py

# Pre-commit won't run unless files have been staged.
git add .

# This must be run on a new project each time it's instantiated in order for linting to pass out of the box. Running it on
# the template itself isn't idempotent when the project is created.
pre-commit run --all-files

echo "Setting up the git repo for the first time"
git commit -am "initial commit" -q
echo "Added everything and committed initially"



#todo - git flow init
echo "-------------------------------------------------------------"
echo "Maybe The Real create_existing_project.sh Was the Friends We Made Along the Way"
echo "-------------------------------------------------------------"
